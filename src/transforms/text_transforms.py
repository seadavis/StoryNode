from core.entity import Reference
from spacy.matcher import Matcher
from utilities.string_functions import remove

def remove_patterns(patterns, pattern_name, nlp, doc):

    matcher = Matcher(nlp.vocab)
    matcher.add(pattern_name, patterns)
    matches = matcher(doc)
   
    spans = []
    adjusted_sentence = doc.text

    for match_id, start, end in matches:
        spans.append(Reference(doc[start:end]))

    for idx, span in enumerate(spans):
        adjusted_sentence = remove(span.start_char, span.end_char, adjusted_sentence)
        span_length = span.end_char - span.start_char

        for count, item in enumerate(spans, start=idx + 1):
            item.start_char = item.start_char - span_length
            item.end_char = item.end_char - span_length
            
    return adjusted_sentence