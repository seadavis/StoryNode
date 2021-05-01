import spacy
from spacy.matcher import Matcher
from .span import TextSpan

class Relation:

    def __init__(self, left_phrase, relation_phrase, right_phrase):
        """Constructs a relation of the form
        (left_phrase, relation_phrase, right_phrase)

        Examples:
        (Sean, runs to, mall), 
        (Gandalf, shall not, pass), 
        (the dog, flies, at midnight)

        Args:
            left_phrase (TextSpan): the leftside phrse
            relation_phrase (TextSpan): the relation phrase
            right_phrase (TextSpan): the right-side phrase of the relation
        """
        self.left_phrase = left_phrase
        self.relation_phrase = relation_phrase
        self.right_phrase = right_phrase

    def __eq__(self, other):
        return self.left_phrase == other.left_phrase and self.relation_phrase == other.relation_phrase and self.right_phrase == other.right_phrase
    
    def __str__(self):
        return f'({self.left_phrase.sentence}, {self.relation_phrase.sentence}, {self.right_phrase.sentence})'


def construct_text_span(doc, start, end):
    span = doc.doc[start:end]
    return TextSpan(span.text, start, end)

def construct_text_spans(doc, matches):
    ret_spans = []
    for match_id, start, end in matches:
        ret_spans.append(construct_text_span(doc, start, end))
    return ret_spans

def extract_relations(doc):
    """extracts the complete relations from the doc

    Args:
        doc ([type]): [description]

    Returns:
        [Relation]: the complete set of relations found from the documentation
    """
    relation_spans = get_relation_spans(doc)
    noun_phrase_pattern = [[{"POS":"NOUN"}], [{"POS": "PROPN"}], [{"POS": "PRON"}]]
    
    relations = []

    for span in relation_spans:
        left_noun = find_nearest_pattern(doc, noun_phrase_pattern, span, True)
        right_noun = find_nearest_pattern(doc, noun_phrase_pattern, span, False)

        if (not left_noun is None) and (not right_noun is None):
            relations.append(Relation(left_noun, span, right_noun))
    return relations
        


def get_relation_spans(doc):
    """extracts the complete relations from the doc

    Args:
        doc (Document): the document we are using to gather
        the middle portion of the relations

    Returns:
        [Relation]: the complete set of relations found from the documentation
    """
    
    
    verbs = get_verbs(doc)
    fluff_pattern = [[{"POS":"VERB"}, {"POS": "PART", "OP": "*"}, {"POS": "ADV", "OP":"*"}], 
                        [{"POS": "VERB"},  {"POS": "ADP", "OP": "*"}, {"POS": "DET", "OP":"*"},
                        {"POS": "AUX", "OP": "*"},  
                        {"POS": "ADJ", "OP":"*"}, {"POS": "ADV", "OP": "*"}]]
    matcher = doc.matcher
    matcher.add("Fluff", fluff_pattern)
    syntactical_constraint_matches = construct_text_spans(doc, matcher(doc.doc))

    relation_spans = []
    for verb in verbs:
        verb_spans = [span for span in syntactical_constraint_matches if verb in span.sentence]
        joined_spans = merge_overlapping_consecutive_word_span(verb_spans)
        longest_span = find_longest_span(joined_spans)
        relation_spans.append(longest_span)
    return relation_spans

        

def get_verbs(doc):
    matcher = doc.matcher
    fluff_pattern = [[{"POS":"VERB"}]]
    matcher.add("Fluff", fluff_pattern)
    matches = matcher(doc.doc)
    verbs = []
    for match_id, start, end in matches:
        verbs.append(doc.doc[start:end].text)
    return verbs

def find_nearest_pattern(doc, pattern, text_span, search_before):
    """Find in doc, the nearest pattern to the given text_span,
    returns the result as a TextSpan

    Args:
        doc (spacy Document) the document in spacy we are looking for
        pattern (the pattern array to search for): the array of patterns we are
        looking for
        text_span (TextSpan): describes where in the document the word or phrase is
        search_before (bool): if true, then we want to find the nearest pattern that occurs,
                before text_span. Otherwise finds the nearest pattern after text_span
    """
    matcher = doc.matcher
    matcher.add("PatternNear", pattern)
    matches = matcher(doc.doc)
    nearest_pattern = None
    spans = construct_text_spans(doc.doc, matches)
    sorted_spans = sorted(spans, key=lambda s : s.start_index)

    spans_to_search = []
    if search_before:
        spans_to_search = [span for span in sorted_spans if span.start_index < text_span.start_index]
        spans_to_search.reverse()

    else:
        spans_to_search = [span for span in sorted_spans if span.start_index > text_span.start_index]

    if len(spans_to_search) == 0:
        return None

    return spans_to_search[0]




def merge_overlapping_consecutive_word_span(text_spans):
    """Merges two spans into one span iff they are
    consecutive end_index=start_index or they overlap

    Applies to all in order.

    Args:
        text_spans ([type]): the span containing the word
    """
    sorted_spans = sorted(text_spans, key=lambda s : s.start_index)
    removal_indices = []
    merged_cons_spans = []

    # first merge the consecutive spans
    for index in range(len(sorted_spans) - 1):

        span = sorted_spans[index]

        if not (index in removal_indices):

            next_index = index + 1
            next_span = sorted_spans[next_index]

            if span.end_index + 1 == next_span.start_index:
                removal_indices.append(next_index)
                merged_cons_spans.append(TextSpan(span.sentence + " " + next_span.sentence, span.start_index, next_span.end_index))
            else:
                merged_cons_spans.append(span)

    last_index = len(sorted_spans) - 1
    if not (last_index in removal_indices):
        merged_cons_spans.append(sorted_spans[last_index])

    current_index = 0
    next_index = 1
    merged_overlapping_spans = []
    overlapped_indices = []

    while next_index <= len(merged_cons_spans) - 1:

        span = merged_cons_spans[current_index]
        next_span = merged_cons_spans[next_index]
        potential_overlap = merge_overlapping_spans(span, next_span)

        if potential_overlap is None:
            current_index = next_index
            next_index = next_index + 1
            merged_overlapping_spans.append(span)
        else:
            overlapped_indices.append(next_index)
            merged_cons_spans[current_index] = potential_overlap
            next_index = next_index + 1

  
    if next_index - current_index > 1:
        merged_overlapping_spans.append(merged_cons_spans[current_index])

    last_cons_index = len(merged_cons_spans) - 1
    if not (last_cons_index in overlapped_indices):
        merged_overlapping_spans.append(merged_cons_spans[last_cons_index])

    if len(merged_overlapping_spans) == 0:
        return merged_cons_spans

    return merged_overlapping_spans
            
                
def merge_overlapping_spans(span_1, span_2):
    """merges the two spans iff and only if they
    are overlapping otherwise returns None

    We assume span_1.start_index <= span_2.start_index

    Args:
        span_1 (TextSpan)
        span_2 (TextSpan)
    """
    if span_1.start_index > span_2.start_index:
        raise Exception("span_1 comes after span_2 when merging overlapping spans")

    if span_2.start_index <= span_1.end_index and span_2.end_index <= span_1.end_index:
        return span_1

    elif span_2.start_index <= span_1.end_index:

        relative_span_1_end = span_1.end_index - span_2.start_index
        span_2_words = span_2.sentence.split()
        remaining_words = span_2_words[(relative_span_1_end):len(span_2_words)]
        entire_string = " ".join(remaining_words)
        return TextSpan(span_1.sentence + " " + entire_string, span_1.start_index, span_2.end_index)

    else:
        return None



def find_latest_span(text_spans):
    """Finds the latest occuring span in given 
    set of text_spans

    Args:
        text_spans (TextSpan): the span of text according to some document
    """
    if len(text_spans) == 0:
        return None

    sorted_spans = sorted(text_spans, key=lambda s: s.end_index, reverse=True)
    return sorted_spans[0]

def find_earliest_span(text_spans):
    """Finds the span that is the "earliest occuriing", i.e. the 
    smallest start index

    Args:
        text_spans ([type]): the smallest match on the text span
    """
    if len(text_spans) == 0:
        return None

    sorted_spans = sorted(text_spans, key=lambda s: s.start_index)
    return sorted_spans[0]


def find_longest_span(text_spans):
    """find the longest match

    Args:
        text_spans ([TextSpan]): the set of matches we are filtering
    """
    if len(text_spans) == 0:
        return None

    sorted_spans = sorted(text_spans, key=lambda s: s.length, reverse=True)
    return sorted_spans[0]


