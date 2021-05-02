import spacy
import sys
from spacy.matcher import Matcher
from src.core.document import Document
from src.core.relation_extraction import *

def test_one_nearest_noun_before():
    doc = Document("Sean is going to the mall")
    nearest_pattern = find_nearest_pattern(doc, 
                        [[{"POS":"NOUN"}], [{"POS": "PROPN"}], [{"POS": "PRON"}]], 
                        TextSpan(doc.doc[2:3]), 
                        True)
    assert nearest_pattern == TextSpan(doc.doc[0:1])

def test_no_nearest_noun_after():
    doc = Document("running throwing hates")
    nearest_pattern = find_nearest_pattern(doc, [[{"POS":"NOUN"}]], doc.span(2, 3), False)
    assert nearest_pattern is None

def test_multiple_nearest_noun_before():
    doc = Document("Sean is going to the mall, and Rochelle is flying a Kite")
    nearest_pattern = find_nearest_pattern(doc, [[{"POS":"NOUN"}], [{"POS": "PROPN"}], [{"POS": "PRON"}]], doc.span(9,10), True)
    assert nearest_pattern == doc.span(8, 9)

def test_one_nearest_noun_after():
    doc = Document("Sean is going to the mall")
    nearest_pattern = find_nearest_pattern(doc, [[{"POS":"NOUN"}], [{"POS": "PROPN"}], [{"POS": "PRON"}]], doc.span(2, 3), False)
    assert nearest_pattern == doc.span(5, 6)

def test_multiple_nearest_noun_after():
    doc = Document("Sean is going to the mall, and Rochelle is flying a Kite")
    nearest_pattern = find_nearest_pattern(doc, [[{"POS":"NOUN"}], [{"POS": "PROPN"}], [{"POS": "PRON"}]], doc.span(2, 3), False)
    assert nearest_pattern == doc.span(5, 6)

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
    doc = Document("Hello sean I'm giving you a high give")
    spans = [doc.span(0, 1), doc.span(3, 5)]
    condensed_spans = merge_overlapping_consecutive_word_span(spans)
    assert len(condensed_spans) == 2

def test_one_span_start_and_ends_before():
    doc = Document("Sean is writing a blog on a saturday")
    spans = [doc.span(2, 6), doc.span(3, 8)]
    condensed_spans = merge_overlapping_consecutive_word_span(spans)
    assert len(condensed_spans) == 1
    assert condensed_spans[0] == doc.span(2, 8)

def test_one_consecutive():
     doc = Document("Sean is going to the mall")
     spans = [doc.span(0, 2), doc.span(2, 3), doc.span(5, 6)]
     condensed_spans = merge_overlapping_consecutive_word_span(spans)
     assert len(condensed_spans) == 2
     assert doc.span(0, 3) == condensed_spans[0]
     assert doc.span(5, 6) == condensed_spans[1]

def test_one_overlap_and_one_consecutive_merge_returns_condensed():

    doc = Document("hello my aunt and me the king with nobles clothes on hats")
    spans = [doc.span(0, 1), 
            doc.span(1, 4), 
            doc.span(9, 11),
            doc.span(6, 12)]
    condensed_spans = merge_overlapping_consecutive_word_span(spans)
    assert len(condensed_spans) == 2
    assert condensed_spans[1] == doc.span(6, 12)

def test_multiple_overlaps_and_multiple_consecutive_merge_returns_condensed():
    doc = Document("word word word going to the mall and titanic I was taken to her immediately bannana gorilla")
    spans = [doc.span(3, 4), doc.span(3, 5), doc.span(3, 7),
            doc.span(11, 15), doc.span(12, 14), doc.span(9, 11)]
    condensed_spans = merge_overlapping_consecutive_word_span(spans)
    assert len(condensed_spans) == 2
    assert condensed_spans[0] == doc.span(3, 7)
    assert condensed_spans[1] == doc.span(9, 15)


def test_empty_find_longest_span_returns_null():
    spans = []
    longest_span = find_longest_span(spans)
    assert longest_span is None

def test_empty_find_earliest_returns_null():
    spans = []
    earliest_span = find_earliest_span(spans)
    assert earliest_span is None


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