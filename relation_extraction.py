import spacy
import sys
from spacy.matcher import Matcher
from src.transforms.text_transforms import remove_patterns
from src.printing.print_tokens import print_token_attributes
from spacy import displacy
from src.core.relation_extraction import *
from src.core.document import *
import os
import functools
import operator

def main(argv):
    
    text_file = argv[1]
    print(text_file)
    f = open(text_file)
    file_lines = f.readlines()

    for line in file_lines:
        doc = Document(line)

        print("Original Text: " + line)
        relations = extract_relations(doc)
        for relation in relations:
            print("Relation: " + str(relation))

        


if __name__ == "__main__":
    main(sys.argv)
