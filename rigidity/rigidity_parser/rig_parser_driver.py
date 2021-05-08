# Token parser driver
import sys
from ..rigidity_lexer import *

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise Exception('usage: %s filename parsername\n' % sys.argv[0])
    filename = sys.argv[1]
    file = open(filename)
    characters = file.read()
    file.close()
    tokens = rig_lex(characters)
    parser = globals()[sys.argv[2]]()
    result = parser(tokens, 0)
    print(result)
