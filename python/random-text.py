
from collections import defaultdict
import random

def create_continuation_map(text):
    cmap = defaultdict(list) # will allow for duplicates
    words = text.split()
    for i in range(len(words)-2):
        cmap[tuple(words[i:i+2])].append(words[i+2])
    return cmap

def reformat(text):
    text = text[text.index('.')+2:text.rindex('.')+1]
    sentences = text.split('. ')
    t = ""
    i = 0
    while i < len(sentences):
        n = i + random.randint(3, 5)
        t += '. '.join(sentences[i:n]) + '.\n\n'
        i = n
    return t[:-3]

def random_text(text, n):
    cmap = create_continuation_map(text)
    s = list(random.choice(cmap.keys()))
    i = 0
    while i < n:
        last = tuple(s[-2:])
        if cmap[last]:
            s.append(random.choice(cmap[last]))
            i += 1
    return reformat(' '.join(s))

text = file('../text/fowler.txt').read()
print random_text(text, 1000)

