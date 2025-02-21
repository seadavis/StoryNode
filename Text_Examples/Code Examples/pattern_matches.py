import spacy
import sys
from spacy.matcher import Matcher
from transforms.text_transforms import remove_patterns
from printing.print_tokens import print_token_attributes
from spacy import displacy
import os
import functools
import operator

def main(argv):
    
    text_file = argv[1]
    print(text_file)
    f = open(text_file)
    file_lines = [f.read()]
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)
    


    for line in file_lines:
    

        # the pattern defined in a paper designed to get at 
        fluff_pattern = [[{"POS":"VERB"}, {"POS": "PART", "OP": "*"}, {"POS": "ADV", "OP":"*"}], 
                        [{"POS": "VERB"},  {"POS": "ADP", "OP": "*"}, {"POS": "DET", "OP":"*"},
                        {"POS": "AUX", "OP": "*"}, {"POS": "NOUN", "OP": "*"}, {"POS": "PRON", "OP": "*"}, 
                        {"POS": "PROPN", "OP":"*"}, {"POS": "ADJ", "OP":"*"}, {"POS": "ADV", "OP": "*"}]]
        matcher.add("Fluff", fluff_pattern)

        doc = nlp(line)
    
    
        matches = matcher(doc)
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]  # Get string representation
            span = doc[start:end]  # The matched span
            print(match_id, string_id, start, end, span.text)

        for token in doc:
            print(token.text, token.pos_, token.dep_, token.i)