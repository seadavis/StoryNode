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

    def intersects(self, other):
        if self.swap_start >= other.swap_start and self.swap_start <= other.swap_end:
            return True
        if self.swap_end >= other.swap_start and self.swap_end <= other.swap_end:
            return True
        if other.swap_start >= self.swap_start and other.swap_start <= self.swap_end:
            return True
        if other.swap_end >= self.swap_start and other.swap_end <= self.swap_end:
            return True
        return False

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

        Does not support swapping the same span twice

        span_1 the span currently in the document.
        span_2 the span being swapped into span_1
    """
    def swap(self, span_1, span_2):
        new_swap = SwapSpan(span_2, span_1)
        self.swap_list.append(new_swap)
        self.swap_list = sorted(self.swap_list, key=lambda s: s.swap_start)

    """
    Prints out the current document
    original_document - if set to true prints out the original document
    before swaps
    """
    def print(self, original_document = False):
        
        if original_document or len(self.swap_list) == 0:
            return self.doc[0:len(self.doc)].text
        
        else:

            printed_doc = ""
            last_swap_end = 0
            last_index = len(self.swap_list) - 1

            for (index, swapped_span) in enumerate(self.swap_list):

                previous_text = ""
                next_text = ""

                if index > 0 and self.swap_list[index - 1].swap_end != swapped_span.swap_start:
                    previous_end = self.swap_list[index - 1].swap_end
                    previous_span = TextSpan(self.doc[previous_end:swapped_span.swap_start])
                    previous_text = previous_span.sentence

                elif index == 0 and swapped_span.swap_start > 0:
                    previous_text = self.doc[0:swapped_span.swap_start].text
            
                swap_text = swapped_span.new_span.sentence
                components = [printed_doc, previous_text, swap_text]
                non_empty_components = (t for t in components if len(t) > 0 and (not t is None))
                printed_doc =  " ".join(non_empty_components)

            last_span = self.swap_list[last_index]
            if last_span.swap_end < len(self.doc):
                next_text = self.doc[swapped_span.swap_end:(len(self.doc))].text
                printed_doc = printed_doc + " " + next_text

            return printed_doc


    def span(self, start, end):
        return TextSpan(self.doc[start:end])
