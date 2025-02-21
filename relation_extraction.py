import sys
from spacy.matcher import Matcher
from src.core.relation_extraction import *
from src.core.document import *


def main(argv):
    
    text_file = argv[1]
    print(text_file)
    f = open(text_file)
    file_contents = f.read()
    doc = Document(file_contents)

    relations = extract_relations(doc)
    for relation in relations:
        print("Relation: " + str(relation))
        print("Type: " + relation.left_phrase.ent_type + ", Right Phrase: " + relation.right_phrase.ent_type) 

       

    
        

              
            

        
if __name__ == "__main__":
    main(sys.argv)
