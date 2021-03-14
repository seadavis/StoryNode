class Reference:

    def __init__(self, span):
        self.start_char = span.start_char
        self.end_char = span.end_char
        self.text = span.text


def print_reference_list(references):

    for ref in references:
        print(ref)