#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Sample a list file. Syntax: sample.py <file> <rate>
E.g.` sample.py foo.list 0.5` will keep half the rows of the file (chosen at random).
The sampled file will be written to the standard output.
"""

import sys
import random

with open(sys.argv[1]) as f:
    l = f.readlines()
    idx = range(len(l))
    size = int(len(l)*float(sys.argv[2]))
    idx_sampled = sorted(random.sample(idx, size))
    l_sampled = [l[i] for i in idx_sampled]
    sys.stdout.write(''.join(l_sampled))
