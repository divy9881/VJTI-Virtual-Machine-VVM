# Entry point for code execution engine
import sys
from .rigidity_lexer import *
from .rigidity_parser import *

def usage():
    sys.stderr.write('Usage: rig filename\n')
    sys.exit(1)

def read_contract_output(contract_id: str):
    print("Contract ID: ", contract_id)
    return contract_id

def call_contract_function(contract_id: str, function_name: str, params: list):
    print("Contract ID: ", contract_id)
    print("Function Name: ", function_name)
    print("Params: ", params)
    return function_name

def send_amount(receiver_address: str, amount: float, message: str):
    print("Address: ", receiver_address)
    print("Amount: ", amount)
    print("Meesage: ", message)
    return message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    filename = sys.argv[1]
    text = open(filename).read()
    tokens = rig_lex(text)
    optimized_tokens = optimize_tokens(tokens)
    # print(optimized_tokens)
    if not optimized_tokens:
        sys.stderr.write('Lex error!\n')
        sys.exit(1)
    parse_result = rig_parse(optimized_tokens)
    if not parse_result:
        sys.stderr.write('Parse error!\n')
        sys.exit(1)

    # print(parse_result)
    ast = parse_result.value
    env = {}

    # print(ast)
    ans = ast.eval(env, dict(), 0, read_contract_output, call_contract_function, send_amount)
    # Here 0 represents the current scope for variables
    # print(ans)

    sys.stdout.write('Final variable values:\n')
    for name in env:
        # print(type(env[name][0]))
        sys.stdout.write('%s: %s\n' % (name, env[name]))
