import spacy
import sys
from spacy.matcher import Matcher
from transforms.text_transforms import remove_patterns
from printing.print_tokens import print_token_attributes
import os
import functools
import operator

def main(argv):
    
    text_file = argv[1]
    print(text_file)
    s = os.getcwd()
    f = open(text_file)
    file_lines = [f.read()]
    nlp = spacy.load("en_core_web_sm")

    fluff_pattern = [[{"POS":"AUX"}],
                    [{"POS":"ADP"}], [{"POS":"DET"}], [{"POS": "PUNCT"}]]
   
    index = 0
    for text in file_lines:
        doc = nlp(text)
        removed_text = remove_patterns(fluff_pattern, "Fluff", nlp, doc)

        relation_pattern = []

        build_relation_patterns("VERB", relation_pattern)
        build_relation_patterns("ADJ", relation_pattern)
        build_relation_patterns("ADV", relation_pattern)          ,

    
        doc = nlp(removed_text)
      
        matcher = Matcher(nlp.vocab)
        matcher.add("Pattern" + str(index), relation_pattern)
        matches = matcher(doc)
        
        print_token_attributes(doc)

        seen_text = []
     
        for match_id, start, end in matches:
            span = doc[start:end]
            if span.text not in seen_text:
                seen_text.append(span.text)
                print(span.text)
        index = index + 1

        
def build_relation_patterns(mid_pos, patterns):
    patterns.append([{"POS": "PROPN", "OP": "+"}, {"POS": mid_pos}, {"POS":"NOUN"}])
    patterns.append([{"POS": "NOUN"}, {"POS": mid_pos}, {"POS":"NOUN"}]) 
    patterns.append([{"POS": "PROPN"}, {"POS": mid_pos}, {"POS":"PROPN"}])
    patterns.append([{"POS": "NOUN"}, {"POS": mid_pos}, {"POS":"PROPN"}])


    


if __name__ == "__main__":
    main(sys.argv)
