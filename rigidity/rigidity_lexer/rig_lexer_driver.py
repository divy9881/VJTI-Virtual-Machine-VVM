# Token extraction driver

import sys
from .rig_lexer import *

if __name__ == '__main__':
    filename = sys.argv[1]
    file = open(filename)
    characters = file.read()
    file.close()
    tokens = rig_lex(characters)
    for token in tokens:
        print(token)
