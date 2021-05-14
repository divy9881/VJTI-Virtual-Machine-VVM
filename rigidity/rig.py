import sys
from .rigidity_lexer import *
from .rigidity_parser import *
import multiprocessing

def usage():
    raise Exception('Usage: rig filename\n')

def read_contract_output(contract_address: str):
    print("Contract Address: ", contract_address)
    return contract_address

def call_contract_function(contract_address: str, function_name: str, params: list):
    print("Contract Address: ", contract_address)
    print("Function Name: ", function_name)
    print("Params: ", params)
    return function_name

def send_amount(receiver_address: str, amount: float, message: str):
    print("Address: ", receiver_address)
    print("Amount: ", amount)
    print("Meesage: ", message)
    return message

def eval(ast, env, read_contract_output, call_contract_function, send_amount, return_dict):
    ans = ast.eval(env, dict(), 0, read_contract_output, call_contract_function, send_amount)   

    sys.stdout.write('Final variable values:\n')
    for name in env:
        sys.stdout.write('%s: %s\n' % (name, env[name]))

    return_dict[0] = str(ans)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    filename = sys.argv[1]
    text = open(filename).read()
    tokens = rig_lex(text)
    print(tokens)
    optimized_tokens = optimize_tokens(tokens)
    if not optimized_tokens:
        raise Exception('Lex error!\n')

    parse_result = rig_parse(optimized_tokens)
    if not parse_result:
        raise Exception('Parse error!\n')

    ast = parse_result.value
    env = {}

    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    try:
        p = multiprocessing.Process(target=eval, args=(ast, env, read_contract_output, call_contract_function, send_amount, return_dict))
        p.start()

        # Wait for 3 seconds or until process finishes
        p.join(3)

        # If thread is still active
        if p.is_alive():

            p.terminate()

            p.join()

            raise RuntimeError("Code took more than 3 seconds!!!!!!!!!")

        print("RESULT : ", return_dict[0])
        
    except Exception as e:
        print("in 2")
        raise e