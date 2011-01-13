#-*- coding: UTF-8 -*-
import os
from yaml import load

def get_yamls(ext='yaml', func=lambda d, f: None):
    for dirname, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith(ext):
                yield func(dirname, 
                           os.path.join(dirname, filename))

for x in get_yamls(func=lambda d, f: load(open(f))):
    print x

