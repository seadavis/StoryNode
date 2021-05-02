import spacy
from spacy.matcher import Matcher
from .span import TextSpan

class Document:

    def __init__(self, text):
        self.nlp = spacy.load("en_core_web_sm")
        self.doc = self.nlp(text)
        self.swap_list = []

    @property
    def matcher(self):
       return Matcher(self.nlp.vocab)


    """
        Swaps span_1 and span_2 widening if needed.

        span_1 the span currently in the document.
        span_2 the span being swapped into span_1
    """
    def swap(self, span_1, span_2):
        return None

    """
    Prints out the current document
    original_document - is set to true prints out the original document
    before swaps
    """
    def print(self, original_document = False):
        return None


    def span(self, start, end):
        return TextSpan(self.doc[start:end])

    """
    gets the span that overlaps with start and end, 
    from the list.

    start - the minimal index form the start of the span
    end - the maximum inex of the swap span
    """
    def get_swap_intersections(self, start, end):
        return None