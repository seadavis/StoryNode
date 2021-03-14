def main(argv):
    nlp = spacy.load("en_core_web_sm")
    text_file = argv[1]
    print(text_file)
    f = open(text_file)
    entire_file = f.read()
    file_lines = entire_file.splitlines()
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)

    for line in file_lines:
        relation_pattern = [{"POS": "PROPN"}, {"POS": "VERB"}, 
                    {"POS":"NOUN"}]
        matcher.add("HelloWorld", [relation_pattern])

        fluff_pattern = [[{"POS":"AUX"}],
                        [{"POS":"ADP"}], [{"POS":"DET"}]]
        matcher.add("Fluff", fluff_pattern)
        doc = nlp(line)
        matches = matcher(doc)
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]  # Get string representation
            span = doc[start:end]  # The matched span
            print(match_id, string_id, start, end, span.text)

        print(line)
        doc = nlp(line)
        for token in doc:
            print(token.text, token.pos_, token.dep_, token.i)

        for ent in doc.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_)