import sys
from typing import List, Any
from .rigidity.rigidity_lexer import *
from .rigidity.rigidity_parser import *
import multiprocessing
import time

class VM:
    def __init__(self, read_contract_output, call_contract_function, send_amount):
        self.read_contract_output = read_contract_output
        self.call_contract_function = call_contract_function
        self.send_amount = send_amount

    def eval(self, ast, env, read_contract_output, call_contract_function, send_amount, return_dict):
        ast.eval(env, dict(), 0, read_contract_output, call_contract_function, send_amount)   
        return_dict[0] = str(env['contract_function_result'])

    def run_function(self, contract_code: str, function_name: str, params_list: List[Any]):
        contract_code.strip('\n ')
        contract_code += ';'
        # print(params_list)
        params = ""
        for p in params_list:
            if type(p) == int:
                params += f"{p}, "
            elif type(p) == str:
                params += f"'{p}', "
            elif type(p) == float:
                params += f"{p}, "
        if len(params) > 0:
            params = params[:-2]
        # print(params)
        contract_code += 'contract_function_result := ' + function_name + '(' + params + ')'

        tokens = rig_lex(contract_code)

        optimized_tokens = optimize_tokens(tokens)
        # print(optimized_tokens)
        if not optimized_tokens:
            raise Exception('Lex error!\n')

        parse_result = rig_parse(optimized_tokens)
        if not parse_result:
     
            raise Exception('Parse error!\n')

        # print(parse_result)
        ast = parse_result.value
        env = {}

        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        try:
            p = multiprocessing.Process(target=eval, args=(ast, env, self.read_contract_output, self.call_contract_function, self.send_amount, return_dict))
            p.start()

            # Wait for 3 seconds or until process finishes
            p.join(3)

            # If thread is still active
            if p.is_alive():

                p.terminate()

                p.join()

                raise RuntimeError("Code took more than 3 seconds!!!!!!!!!")

            return return_dict[0]
        except Exception as e:
            raise e
