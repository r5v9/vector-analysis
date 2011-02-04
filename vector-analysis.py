
from collections import defaultdict
import sys, math

def create_count_map(text):
    cmap = defaultdict(int)
    
    for i in range(len(text)-2):
        cmap[text[i:i+3]] += 1

    return cmap

def modulus(cmap, reference_cmap):
    m = 0
    for trigram in cmap:
        if trigram in reference_cmap:
            m += cmap[trigram] ** 2
    return m ** 0.5

def inner_product(cmap, reference_cmap):
    inner = 0
    for trigram in cmap:
        inner += cmap[trigram] * reference_cmap[trigram]
    return inner

def angle(cmap, reference_cmap):
    return inner_product(cmap, reference_cmap) / ( modulus(cmap, reference_cmap) * modulus(reference_cmap, reference_cmap) ) 

def build_references_map(languages):
    references_map = {}    
    for language in languages:
        references_map[language] = create_count_map(file(language + '.txt').read())
    return references_map       

def find_language(text, references_map):
    cmap = create_count_map(text)
    max_angle, max_language = -sys.maxint, "unknown"
    for language, language_cmap in references_map.iteritems():
        a = angle(cmap, language_cmap)
        print '%s in %s vector space: %f' % (text[0:2], language, math.degrees(math.acos(a)))
        if a > max_angle:
            max_angle, max_language = a, language
    return max_language

# -------------------- tests --------------------

import unittest

class TestVectorAnalysis(unittest.TestCase):

    def test_create_count_map(self):

        self.assertEqual(create_count_map(''), {})
        self.assertEqual(create_count_map('a'), {})
        self.assertEqual(create_count_map('abc'), {'abc':1})
        self.assertEqual(create_count_map('abcd'), {'abc':1, 'bcd':1})
        self.assertEqual(create_count_map('abcabc'), {'abc':2, 'bca':1, 'cab':1})

    def test_modulus(self):

        cmap = {'abc':3, 'bca':4, 'xxx':8 }
        reference_cmap = {'abc':7, 'bca':9 }
        self.assertEqual(5, modulus(cmap, reference_cmap))

    def test_inner_product(self):
        cmap = defaultdict(int)
        cmap.update(dict(abc=2, bca=4, xxx=8))

        reference_cmap = defaultdict(int)
        reference_cmap.update(dict(abc=7, bca=9))

        self.assertEqual(50, inner_product(cmap, reference_cmap))

    def test_angle(self):
        cmap = defaultdict(int)
        cmap.update(dict(abc=3, bca=4, xxx=8))

        reference_cmap = defaultdict(int)
        reference_cmap.update(dict(abc=3, bca=2))

        self.assertTrue("0.500", "%.3f" % modulus(cmap, reference_cmap))

    def test_find_language(self):
        languages = ('english', 'french', 'latin', 'spanish', 'portuguese', 'italian', 'german')
        references_map = build_references_map(languages)
        for language in languages: 
            text = ' '.join(file(language + '-sample.txt').read().split()[:15])
            self.assertEqual(language, find_language(text, references_map))

if __name__ == '__main__':
    unittest.main()

