class TextSpan:

    def __init__(self, sentence, start_index, end_index):
        self.sentence = sentence
        self.start_index = start_index
        self.end_index = end_index

    @property
    def length(self):
        return self.end_index - self.start_index

    def __eq__(self, other):
        return self.sentence == other.sentence and self.start_index == self.start_index and self.end_index == self.end_index

    """
    Gives a deep copy of the text span
    """
    def copy(self):
        return None
    
    """

    Replaces the text starting at start to be other,
    widening if needed.

    other - the other text span to replace either this span or this entire span with
    start - the index to start the replacing. 0-based.

    """
    def replace(self, other, start):
        return ""