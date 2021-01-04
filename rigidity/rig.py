# Entry point for code execution engine
import sys
from .rigidity_lexer import *
from .rigidity_parser import *
import pprint as pp

def usage():
    sys.stderr.write('Usage: rig filename\n')
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    filename = sys.argv[1]
    text = open(filename).read()
    tokens = rig_lex(text)
    optimized_tokens = optimize_tokens(tokens)
    if not optimized_tokens:
        sys.stderr.write('Lex error!\n')
        sys.exit(1)
    # print(optimized_tokens)
    parse_result = rig_parse(optimized_tokens)
    if not parse_result:
        sys.stderr.write('Parse error!\n')
        sys.exit(1)
    # pp.pprint("Parse Result :")
    # pp.pprint(parse_result)
    ast = parse_result.value
    # pp.pprint("AST : ")
    # pp.pprint(ast)
    env = {}
    ast.eval(env)
    # pp.pprint("ENV : ")
    # pp.pprint(env)
    # pp.pprint("AST : ")
    # pp.pprint(ast)
    sys.stdout.write('Final variable values:\n')
    for name in env:
        sys.stdout.write('%s: %s\n' % (name, env[name]))
