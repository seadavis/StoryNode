import spacy
from spacy.matcher import Matcher

class Document:

    def __init__(self, text):
        self.nlp = spacy.load("en_core_web_sm")
        self.doc = self.nlp(text)

    @property
    def matcher(self):
       return Matcher(self.nlp.vocab)


    """
        Swaps out span_1 and span_2 widening if needed.

        span_1 the span currently in the document.
        span_2 the span being swapped into span_1
    """
    def swap(span_1, span_2):
        return None

    """
        span - the text span we want to insert and replace.
        start_index - the index we want to start replacing with
    """
    def replace(span, start_index):
        return ""

    def shift(self, start_index, shift_amount):
        return None

       