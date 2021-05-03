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
    span_swap = doc2.span(6, 7)
    doc.swap(span, span_swap)
    new_text = doc.print()
    assert new_text == "Python code hello the cleanest code around unlike C++ which is garbage nonsense"


def test_multiple_replacements():

    sample_text = "Python code is the cleanest code around unlike C++ which is garbage nonsense"
    doc = Document(sample_text)
    span = doc.span(5, 6)
    span2 = doc.span(12, 13)
    span3 = doc.span(8, 10)

    doc2 = Document("the joker fights guys batman is evil")
    doc3 = Document("highlighting textbooks for fun")
    span_swap = doc2.span(4, 5)
    span_swap2 = doc3.span(0, 1)
    span_swap3 = doc3.span(1, 3)

    doc.swap(span, span_swap)
    doc.swap(span2, span_swap2)
    doc.swap(span3, span_swap3)

    new_text = doc.print()
    assert new_text == "Python code is the cleanest batman around unlike textbooks for is garbage highlighting"

def test_one_to_one_replacement_same_start_end():
    sample_text = "Python code is the cleanest code around unlike C++ which is garbage nonsense"
    doc = Document(sample_text)
    span = doc.span(5, 6)
    doc2 = Document("the joker fights guys batman is evil")
    span_swap = doc2.span(4, 5)
    doc.swap(span, span_swap)
    new_text = doc.print()
    assert new_text == "Python code is the cleanest batman around unlike C++ which is garbage nonsense"

def test_n_to_n_replacement():
    sample_text = "Python code is the cleanest code around unlike C++ which is garbage nonsense"
    doc = Document(sample_text)
    span = doc.span(0, 7)
    doc2 = Document("my adult nephew enjoys crafts and cutting paper like a two year old")
    span_swap = doc2.span(6, 14)
    doc.swap(span, span_swap)
    new_text = doc.print()

    assert new_text == "cutting paper like a two year old unlike C++ which is garbage nonsense"

def test_n_to_n_replacement_same_start_end():
    sample_text = "Python code is the cleanest code around unlike C++ which is garbage nonsense"
    doc = Document(sample_text)
    span = doc.span(6, 9)
    doc2 = Document("my mom told me to button up jacket young man its cold outside")
    span_swap = doc2.span(5, 9)
    doc.swap(span, span_swap)
    new_text = doc.print()
    assert new_text == "Python code is the cleanest code button up jacket young which is garbage nonsense"

def test_shorter_replacement():
    sample_text = "Python code is the cleanest code around unlike C++ which is garbage nonsense"
    doc = Document(sample_text)
    span = doc.span(4, 9)
    doc2 = Document("down dog, get off of the couch")
    span_swap = doc2.span(0, 2)
    doc.swap(span, span_swap)
    new_text = doc.print()
    assert new_text == "Python code is the down dog which is garbage nonsense"


def test_longer_replacement():
    sample_text = "Python code is the cleanest code around unlike C++ which is garbage nonsense"
    doc = Document(sample_text)
    span = doc.span(8, 10)
    doc2 = Document("my mom told me to button up jacket young man its cold outside")
    span_swap = doc2.span(5,12)
    doc.swap(span, span_swap)
    new_text = doc.print()
    assert new_text == "Python code is the cleanest code around unlike button up jacket young man its cold is garbage nonsense"


def test_original_still_prints_after_replacement():
    sample_text = "Python code is the cleanest code around unlike C++ which is garbage nonsense"
    doc = Document(sample_text)
    span = doc.span(8, 10)
    doc2 = Document("my mom told me to button up jacket young man its cold outside")
    span_swap = doc2.span(5,12)
    doc.swap(span, span_swap)
    old_text = doc.print(True)
    assert old_text == sample_text
