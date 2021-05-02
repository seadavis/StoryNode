import spacy
from spacy.matcher import Matcher
from .span import TextSpan

"""
 Class that represents how to 
 swap a span into and out of a document
"""
class SwapSpan:

    """
    swapped_span - the span being "swapped out" or the old span
    new_span - the span being "swapped in" or the new span
    """
    def __init__(self, new_span, swapped_span):
        self.span = span
        self.new_span = new_span
        self.swapped_span = swapped_span

    @property
    def swap_start(self):
        return self.swapped_span.start_index

    @property
    def swap_end(self):
        return self.swapped_span.end_index

    def swapped_text(self):
        return self.new_span.sentence

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
        self.swap_list = self.swap_list.append(SwappedSpans(span_2, span_1)

    """
    Prints out the current document
    original_document - is set to true prints out the original document
    before swaps
    """
    def print(self, original_document = False):
        if original_document or len(self.swap_list) == 0:
            return self.doc[0:len(self.doc)].text
        else:

            printed_doc = ""

            for (index, span) in self.swap_list:

                swapped_start = span.swap_start
                swapped_end = span.swapped_end
                printed_doc = self.doc[last_swapped_end:swapped_start].text + span.swapped_text + self.doc[swapped_end]

            return printed_doc



    def span(self, start, end):
        return TextSpan(self.doc[start:end])

    """
    gets the spans from
    the swap list that intersect the given
    span

    """
    def get_swap_intersections(self, span):
        return (s for s in self.swap_list if s.intersects(span))

