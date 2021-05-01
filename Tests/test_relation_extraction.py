import spacy
import sys
from spacy.matcher import Matcher
from src.core.document import Document
from src.core.relation_extraction import *

def test_one_nearest_noun_before():
    doc = Document("Sean is going to the mall")
    nearest_pattern = find_nearest_pattern(doc, 
                        [[{"POS":"NOUN"}], [{"POS": "PROPN"}], [{"POS": "PRON"}]], 
                        TextSpan("going", 2, 3), 
                        True)
    assert nearest_pattern == TextSpan("Sean", 0, 1)

def test_no_nearest_noun_after():
    doc = Document("running throwing hates")
    nearest_pattern = find_nearest_pattern(doc, [[{"POS":"NOUN"}]], TextSpan("throwing", 2, 3), False)
    assert nearest_pattern is None

def test_multiple_nearest_noun_before():
    doc = Document("Sean is going to the mall, and Rochelle is flying a Kite")
    nearest_pattern = find_nearest_pattern(doc, [[{"POS":"NOUN"}], [{"POS": "PROPN"}], [{"POS": "PRON"}]], TextSpan("flying", 9, 10), True)
    assert nearest_pattern == TextSpan("Rochelle", 7, 8)

def test_one_nearest_noun_after():
    doc = Document("Sean is going to the mall")
    nearest_pattern = find_nearest_pattern(doc, [[{"POS":"NOUN"}], [{"POS": "PROPN"}], [{"POS": "PRON"}]], TextSpan("going", 2, 3), False)
    assert nearest_pattern == TextSpan("mall", 5, 6)

def test_multiple_nearest_noun_after():
    doc = Document("Sean is going to the mall, and Rochelle is flying a Kite")
    nearest_pattern = find_nearest_pattern(doc, [[{"POS":"NOUN"}], [{"POS": "PROPN"}], [{"POS": "PRON"}]], TextSpan("going", 2, 3), False)
    assert nearest_pattern == TextSpan("mall", 5, 6)

def test_empty_doc_get_verb_returns_none():
    doc = Document("")
    verbs = get_verbs(doc)
    assert len(verbs) == 0

def test_no_verbs_get_verbs_returns_none():
    doc = Document("Sean is The mall")
    verbs = get_verbs(doc)
    assert len(verbs) == 0

def test_one_verb_get_verbs_returns_verb():
    doc = Document("Sean is going to the mall")
    verbs = get_verbs(doc)
    assert len(verbs) == 1
    assert verbs[0] == "going"

def test_multiple_verbs():
    doc = Document("Sean is going to the mall. Rochelle is running errands. Ducks are flying south")
    verbs = get_verbs(doc)
    assert len(verbs) == 3
    assert verbs[0] == "going"
    assert verbs[1] == "running"
    assert verbs[2] == "flying"

def test_none_overlapping_merge_returns_same_list():
    spans = [TextSpan("hello", 1, 2), TextSpan("weretak", 5, 12)]
    condensed_spans = merge_overlapping_consecutive_word_span(spans)
    assert len(condensed_spans) == 2

def test_one_span_start_and_ends_before():
    spans = [TextSpan("is writing a blog", 2, 6), TextSpan("writing a blog on a", 3, 8)]
    condensed_spans = merge_overlapping_consecutive_word_span(spans)
    assert len(condensed_spans) == 1
    assert condensed_spans[0] == TextSpan("is writing a blog on a", 2, 8)

def test_one_consecutive():
     spans = [TextSpan("going to", 3, 5), TextSpan("the mall", 6, 7), TextSpan("Davey", 120, 121)]
     condensed_spans = merge_overlapping_consecutive_word_span(spans)
     assert len(condensed_spans) == 2
     assert TextSpan("going to the mall", 3, 7) == condensed_spans[0]
     assert TextSpan("Davey", 120, 121) == condensed_spans[1]

def test_one_overlap_and_one_consecutive_merge_returns_condensed():
    spans = [TextSpan("hello", 1, 2), 
            TextSpan("my aunt and", 5, 8), 
            TextSpan("the king with nobles clothes on hats", 9, 16), 
            TextSpan("and me the king with nobles clothes", 7, 14)]
    condensed_spans = merge_overlapping_consecutive_word_span(spans)
    assert len(condensed_spans) == 2
    assert condensed_spans[1] == TextSpan("my aunt and me the king with nobles clothes on hats", 5, 16)

def test_multiple_overlaps_and_multiple_consecutive_merge_returns_condensed():
    spans = [TextSpan("going", 3, 4), TextSpan("going to", 3, 5), TextSpan("going to the mall", 3, 7),
            TextSpan("taken to her immediately", 18, 22), TextSpan("to her", 19, 21), TextSpan("I was", 16, 18)]
    condensed_spans = merge_overlapping_consecutive_word_span(spans)
    assert len(condensed_spans) == 2
    assert condensed_spans[0] == TextSpan("going to the mall", 3, 7)
    assert condensed_spans[1] == TextSpan("I was taken to her immediately", 16, 22)


def test_overlap_non_adjacent_still_condenses():
    spans = [TextSpan("going", 3, 4), TextSpan("going to", 3, 5), TextSpan("going to the mall", 3, 7),
            TextSpan("taken to her immediately", 18, 22), TextSpan("to her", 19, 20), TextSpan("I was", 16, 17)]
    condensed_spans = merge_overlapping_consecutive_word_span(spans)
    assert len(condensed_spans) == 2
    assert condensed_spans[0] == TextSpan("going to the mall", 3, 7)
    assert condensed_spans[1] == TextSpan("I was taken to her immediately", 16, 22)

def test_consecutive_non_adjacent_still_condenses():
    spans = [TextSpan("going", 3, 4), 
            TextSpan("taken to her immediately", 18, 22), TextSpan("going to", 3, 5), TextSpan("going to the mall", 3, 7), TextSpan("I was", 16, 18)]
    
    condensed_spans = merge_overlapping_consecutive_word_span(spans)
    assert len(condensed_spans) == 2
    assert condensed_spans[0] == TextSpan("going to the mall", 3, 7)
    assert condensed_spans[1] == TextSpan("I was taken to her immediately", 16, 22)

def test_empty_find_longest_span_returns_null():
    spans = []
    longest_span = find_longest_span(spans)
    assert longest_span is None

def test_empty_find_earliest_returns_null():
    spans = []
    earliest_span = find_earliest_span(spans)
    assert earliest_span is None

def test_find_earliest():
    spans = [TextSpan("going", 3, 4), TextSpan("going to", 3, 5), TextSpan("going to the mall", 3, 7),
            TextSpan("taken to her immediately", 18, 22), TextSpan("to her", 19, 20), TextSpan("I was", 16, 17)]
    earliest_span = find_earliest_span(spans)
    assert earliest_span == TextSpan("going", 3, 4)

def test_empty_find_latest_returns_null():
    spans = []
    latest_span = find_latest_span(spans)
    assert latest_span is None

def test_find_latest():
    spans = [TextSpan("going", 3, 4), TextSpan("going to", 3, 5), TextSpan("going to the mall", 3, 7),
            TextSpan("taken to her immediately", 18, 22), TextSpan("to her", 19, 20), TextSpan("I was", 16, 17)]
    latest_span = find_latest_span(spans)
    assert latest_span == TextSpan("taken to her immediately", 18, 22)

def test_non_empty_find_longest_span_returns_longest():
    spans = [TextSpan("going", 3, 4), TextSpan("going to", 3, 5), TextSpan("going to the mall", 3, 7),
            TextSpan("taken to her immediately tomorrow", 18, 23), TextSpan("to her", 19, 20), TextSpan("I was", 16, 17)]
    longest_span = find_longest_span(spans)
    assert longest_span == TextSpan("taken to her immediately tomorrow", 18, 23)

def test_one_find_longest_span_returns_single():
    spans = [TextSpan("going", 3, 4)]
    longest_span = find_longest_span(spans)
    assert longest_span == TextSpan("going", 3, 4)

def test_simple_examples():
    doc = Document("Sean, is going to the mall")
    relations = extract_relations(doc)
    assert str(relations[0]) == "(Sean, going to the, mall)"

    doc = Document("Elizabeth was glad to be taken to her immediately")
    relations = extract_relations(doc)
    assert str(relations[0]) == "(Elizabeth, taken to, her)"

def test_multiple_examples():
    doc = Document("In July 2012, Ancestry.com found a strong likelihood that Dunham was descended from John Punch")
    relations = extract_relations(doc)
    assert str(relations[0]) == "(Ancestry.com, found a strong, likelihood)"
    assert str(relations[1]) == "(Dunham, descended from, John)"