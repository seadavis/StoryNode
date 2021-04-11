import spacy
import sys
from spacy.matcher import Matcher
from transforms.text_transforms import remove_patterns
from printing.print_tokens import print_token_attributes
from spacy import displacy
from core.relation_extraction import *
import os
import functools
import operator

def main(argv):
    
    text_file = argv[1]
    print(text_file)
    f = open(text_file)
    file_lines = f.readlines()
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)

    for line in file_lines:
        doc = nlp(line)

        print("Original Text: " + line)
        relations = extract_relations(doc)
        for relation in relations:
            print("Relation: " + str(relation))

        


if __name__ == "__main__":
    main(sys.argv)
