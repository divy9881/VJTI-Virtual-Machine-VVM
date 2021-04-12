import sys
from rigidity.rigidity_lexer import *
from rigidity.rigidity_parser import *

class VM:
    def __init__(self, read_contract_output, call_contract_function, send_amount):
        self.read_contract_output = read_contract_output
        self.call_contract_function = call_contract_function
        self.send_amount = send_amount

    def run_function(self, contract_code: str, function_name: str, params_stringified_json: list):
        contract_code.strip('\n ')
        contract_code += ';'
        contract_code += 'contract_function_result := ' + function_name + '(' + ','.join(params_stringified_json) + ')'

        tokens = rig_lex(contract_code)

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
        ast.eval(env, dict(), 0, self.read_contract_output, self.call_contract_function, self.send_amount)
        
        return str(env['contract_function_result'])

