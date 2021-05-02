import spacy
from spacy.matcher import Matcher
import sys

def main(argv):
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)
    # Add match ID "HelloWorld" with no callback and one pattern
    pattern = [{"LOWER": "hello"}, {"IS_PUNCT": True}, {"LOWER": "world"}]
    matcher.add("HelloWorld", [pattern])

    doc = nlp("Hello, world! Hello world!")
    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        print(match_id, string_id, start, end, span.text)
    
    doc[0:1] = "goodbye"

    print(doc[0:5])


if __name__ == "__main__":
    main(sys.argv)