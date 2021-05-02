class TextSpan:

    def __init__(self, span):
        self.span = span

    @property
    def length(self):
        return self.end_index - self.start_index

    @property
    def sentence(self):
        return self.span.text

    @property
    def start_index(self):
        return self.span.start
    
    @property
    def end_index(self):
        return self.span.end

    def __eq__(self, other):
        return self.sentence == other.sentence and self.start_index == self.start_index and self.end_index == self.end_index

    def join(self, other):

        if not self.intersects(other):
            return None

        min_start = min(self.start_index, other.start_index)
        max_end = max(self.end_index, other.end_index)
        
        return TextSpan(self.span.doc[min_start:max_end])

    """
    Takes the subset of the start_index, end_index
    start_index - the starting index of the subset, relative
    to the spans parent document

    end_index - the ending index of the subset, relative 
    to the spans partner document
    """    
    def subset(self, start_index, end_index):
        return TextSpan(self.span.doc[start_index:end_index])

    """
    Returns true if the given span intersects with this span.
    False otherwise.
    """
    def intersects(self, other):
        if self.start_index >= other.start_index and self.start_index <= other.end_index:
            return True
        if self.end_index >= other.start_index and self.end_index <= other.end_index:
            return True
        if other.start_index >= self.start_index and other.start_index <= self.end_index:
            return True
        if other.end_index >= self.start_index and other.end_index <= self.end_index:
            return True
        return False
        
        