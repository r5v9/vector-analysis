#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import re

def cleanup():
        text = re.sub(' +', ' ', re.sub('[\[\]\(\)\-\.\,\r\n\"\'"”„–;]', ' ', file('x.txt').read())).lower().strip()
        text = str(text)
        file('y.txt', 'w').write(text)

cleanup()
