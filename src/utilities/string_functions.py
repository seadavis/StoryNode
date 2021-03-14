"""
Swaprs token1, for token2 in the sentence
token2 should belong in sentence for this to work
"""
def swap(token1, token2, sentence):
    index = token2.idx
    length = len(token2.text)
    if index == 0:
        prepend = ''
    else:
        prepend = sentence[:(index)]
    append = sentence[(index + length):]
    return prepend + token1.text + append

def remove(token, sentence):
    return remove(token.idx, token.idx + len(token.text), sentence)
   
"""
Removes all characters 
from start to end in sentence
"""
def remove(start, end, sentence):
    append = sentence[end:(len(sentence))]
    prepend = ''
    if start > 0:
        prepend = sentence[:(start)]
    return prepend + append