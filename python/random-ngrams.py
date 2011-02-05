
from collections import defaultdict
import random

def create_continuation_map(text, ng=2):
    cmap = defaultdict(list) # will allow for duplicates
    for i in range(len(text)-ng):
        cmap[text[i:i+ng]].append(text[i+ng])
    return cmap

def random_text(text, n, ng=2):
    cmap = create_continuation_map(text, ng)
    s = random.choice(cmap.keys())
    for i in range(n):
        last = s[-ng:]
        if cmap[last]:
            s += random.choice(cmap[last])
    return s


text = file('../text/english.txt').read()
print random_text(text, 500, 3)

