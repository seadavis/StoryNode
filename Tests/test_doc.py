import spacy
import sys
from spacy.matcher import Matcher
from src.core.document import Document
from src.core.relation_extraction import *

def test_one_to_one_replacement():
    sample_text = "Python code is the cleanest code around unlike C++ which is garbage nonsense"
    doc = Document(sample_text)
    doc2 = Document("word word word word word word hello")
    span = doc.span(2, 3)
    span_swap = doc2.span(7, 8)
    doc.swap(span, span_swap)
    new_text = doc.print()
    assert new_text == "Python code hello the cleanest code around unlike C++ which is garbage nonsense"

    new_span = doc.span(2, 3)
    old_span = doc.span(4, 5)
    assert new_span.sentence == "hello"
    assert old_span.sentence == "cleanest"
  

def test_one_to_one_replacement_same_start_end():
    sample_text = "Python code is the cleanest code around unlike C++ which is garbage nonsense"
    doc = Document(sample_text)
    span = doc.span(5, 6)
    doc2 = Document("the joker fights guys batman is evil")
    span_swap = doc2.span(5, 6)
    doc.swap(span, span_swap)
    new_text = doc.print()
    assert new_text == "Python code is the cleanest batman around unlike C++ which is garbage nonsense"

def test_n_to_n_replacement():
    sample_text = "Python code is the cleanest code around unlike C++ which is garbage nonsense"
    doc = Document(sample_text)
    span = doc.span(0, 7)
    doc2 = Document("my adult nephew enjoys crafts and cutting paper like a two year old")
    span_swap = doc2.span(7, 14)
    doc.swap(span, span_swap)
    new_text = doc.print()

    new_span = doc.span(3, 6)
    old_span = doc.span(9, 11)
    assert new_span.sentence == "a two year old"
    assert old_span.sentence == "which is"
    assert new_text == "cutting paper like a two year old unlike C++ which is garbage nonsense"

def test_n_to_n_replacement_same_start_end():
    sample_text = "Python code is the cleanest code around unlike C++ which is garbage nonsense"
    doc = Document(sample_text)
    span = doc.span(6, 9)
    doc2 = Document("my mom told me to button up jacket young man its cold outside")
    span_swap = doc2.span(6, 9)
    doc.swap(span, span_swap)
    new_text = doc.print()
    assert new_text == "Python code is the cleanest code button up jacket which is garbage nonsense"

def test_shorter_replacement():
    sample_text = "Python code is the cleanest code around unlike C++ which is garbage nonsense"
    doc = Document(sample_text)
    span = doc.span(4, 9)
    doc2 = Document("down dog, get off of the couch")
    span_swap = doc2.span(0, 1)
    doc.swap(span, span_swap)
    new_text = doc.print()
    assert new_text == "Python code is the down dog which is garbage nonsense"

    new_span = doc.span(4, 6)
    old_span = doc.span(7, 10)
    assert new_span.sentence == "down dog"
    assert old_span.sentence == "which is garbage"


def test_longer_replacement():
    sample_text = "Python code is the cleanest code around unlike C++ which is garbage nonsense"
    doc = Document(sample_text)
    span = doc.span(8, 10)
    doc2 = Document("my mom told me to button up jacket young man its cold outside")
    span_swap = doc2.span(5,12)
    doc.swap(span, span_swap)
    new_text = doc.print()
    assert new_text == "Python code is the cleanest code around unlike button up jacket young man its cold outside is garbage nonsense"

    new_span = doc.span(7, 11)
    old_span = doc.span(16, 19)
    assert new_span.sentence == "unlike button up jacket young"
    assert old_span.sentence == "is garbage nonsense"

def test_original_still_prints_after_replacement():
    sample_text = "Python code is the cleanest code around unlike C++ which is garbage nonsense"
    doc = Document(sample_text)
    span = doc.span(8, 10)
    doc2 = Document("my mom told me to button up jacket young man its cold outside")
    span_swap = doc2.span(5,12)
    doc.swap(span, span_swap)
    old_text = doc.print(True)
    assert old_text == sample_text

def test_swap_twice():
    sample_text = "Python code is the cleanest code around unlike C++ which is garbage nonsense"
    doc = Document(sample_text)
    span = doc.span(4, 9)
    doc2 = Document("down dog get off of the couch")
    span_swap = doc2.span(0, 4)
    doc.swap(span, span_swap)

    doc3 = Document("elvis was much larger than life")
    second_span_swap = doc3.span(3, 6)
    doc.swap(span, second_span_swap)
    new_text = doc.print()
    assert new_text == "Python code is the larger than life off which is garbage nonsense"

    new_span = doc.span(4, 7)
    old_span = doc.span(7, 10)
    assert new_span.sentence == "larger than life off"
    assert old_span.sentence == "off which is"