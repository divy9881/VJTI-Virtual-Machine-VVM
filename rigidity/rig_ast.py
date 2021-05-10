from .equality import *
import sys
import time

def check(params, env):
    for i in range(0, len(params)):
        if type(params[i]) == list:
            if params[i][0] in env:
                params[i] = env[params[i][0]]
            else:
                raise NameError("Identifier not found")
    return params

class Statement(Equality):
    pass

class Aexp(Equality):
    pass

class Bexp(Equality):
    pass

class Routine:
    def __init__(self, params, body):
        self.params = params
        self.body = body

    def __repr__(self):
        return 'Routine(%s, %s)' % (self.params, self.body)

# Assignment statement
class AssignStatement(Statement):
    def __init__(self, name, aexp):
        self.name = name
        self.aexp = aexp

    def __repr__(self):
        return 'AssignStatement(%s, %s)' % (self.name, self.aexp)

    def eval(self, env, scope_map, scope, read_contract_output, call_contract_function, send_amount):
        value = self.aexp.eval(env, scope_map, scope, read_contract_output, call_contract_function, send_amount)
        # Here if the name exists then we only change the value and no the scope
        # If not present we create a new entry
        
        if '[' in self.name:
            dict_name = self.name[: self.name.index('[')]
            key_name = self.name[self.name.index('[') + 1: self.name.index(']')]

            if dict_name in env:
                # For float as a key
                if '.' in key_name:
                    key = float(key_name)
                    env[dict_name][key] = value

                #For string as a key
                elif '\'' in key_name:
                    key = str(key_name[1:-1])
                    env[dict_name][key] = value

                #For int as key
                else:
                    if key_name.isnumeric():
                        key = int(key_name)
                        env[dict_name][key] = value
                    else:
                        raise TypeError('key must be either integers, float or string')
            else:
                raise NameError('name ' + dict_name + ' is not defined in this scope')
        else:                             
            if self.name in env:
                env[self.name] = value
            else:
                env[self.name] = value
                if scope in scope_map:
                    scope_map[scope].append(self.name)
                else:
                    scope_map[scope] = []
                    scope_map[scope].append(self.name)

# Compound statement
class CompoundStatement(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return 'CompoundStatement(%s, %s)' % (self.first, self.second)

    def eval(self, env, scope_map, scope, read_contract_output, call_contract_function, send_amount):
        x = self.first.eval(env, scope_map, scope, read_contract_output, call_contract_function, send_amount)
        y = self.second.eval(env, scope_map, scope, read_contract_output, call_contract_function, send_amount)
        if x != None:
            return x
        if y != None:
            return y

# If statement
class IfStatement(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt

    def __repr__(self):
        return 'IfStatement(%s, %s, %s)' % (self.condition, self.true_stmt, self.false_stmt)

    def eval(self, env, scope_map, scope, read_contract_output, call_contract_function, send_amount):
        condition_value = self.condition.eval(env, scope_map, scope, read_contract_output, call_contract_function, send_amount)
        if condition_value:
            x = self.true_stmt.eval(env, scope_map, scope + 1, read_contract_output, call_contract_function, send_amount)
            if x != None:
                return x
        else:
            if self.false_stmt:
                x = self.false_stmt.eval(env, scope_map, scope + 1, read_contract_output, call_contract_function, send_amount)
                if x != None:
                    return x
        
        # This loop add names of variable that were declared in if statement
        # names_to_be_removed = []
        # for name in env:
        #     if env[name][1] > scope:
        #         names_to_be_removed.append(name)
        
        # This loop removes the names from env
        # for name in names_to_be_removed:
        #     env.pop(name)

        # sorted_keys = scope_map.keys().sort()
        # length = len(sorted_keys)

        if scope + 1 in scope_map:
            for i in scope_map[scope+1]:
                env.pop(i)
            scope_map.pop(scope+1)


# While Statement
class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'WhileStatement(%s, %s)' % (self.condition, self.body)

    def eval(self, env, scope_map, scope, read_contract_output, call_contract_function, send_amount):
        condition_value = self.condition.eval(env, scope_map, scope, read_contract_output, call_contract_function, send_amount)
        while condition_value:
            x = self.body.eval(env, scope_map, scope + 1, read_contract_output, call_contract_function, send_amount)
            if x != None:
                return x
            condition_value = self.condition.eval(env, scope_map, scope, read_contract_output, call_contract_function, send_amount)

        # This loop add names of variable that were declared in while statement
        # names_to_be_removed = []
        # for name in env:
        #     if env[name][1] > scope:
        #         names_to_be_removed.append(name)
        
        # This loop removes the names from env
        # for name in names_to_be_removed:
        #     env.pop(name)        

        if scope + 1 in scope_map:
            for i in scope_map[scope+1]:
                env.pop(i)
            scope_map.pop(scope+1)

# Function Statement
class FunctionStatement(Statement):
    def __init__(self, func, body):
        self.name = func.name
        self.params = [x[0] for x in func.params]
        self.body = body

    def __repr__(self):
        return 'FunctionStatement(%s, %s, %s)' % (self.name, self.params, self.body)

    def eval(self, env, scope_map, scope, read_contract_output, call_contract_function, send_amount):
        if self.name in env:
            raise NameError("Function Already Exists!!!")
        else:
            env[self.name] = Routine(self.params, self.body)
            if scope in scope_map:
                scope_map[scope].append(self.name)
            else:
                scope_map[scope] = []
                scope_map[scope].append(self.name)

# Function Call Statement
class FunctionCallStatement(Statement):
    def __init__(self, func):
        self.func = func

    def __repr__(self):
        return 'FunctionCallStatement(%s)' % (self.func)

    def eval(self, env, scope_map, scope, read_contract_output, call_contract_function, send_amount):
        x = self.func.eval(env, scope_map, scope, read_contract_output, call_contract_function, send_amount)
        if x != None:
            return x

# Return Statement
class ReturnStatement(Statement):
    def __init__(self, aexp):
        self.aexp = aexp

    def __repr__(self):
        return 'ReturnStatement(%s)' % (self.aexp)

    def eval(self, env, scope_map, scope, read_contract_output, call_contract_function, send_amount):
        return self.aexp.eval(env, scope_map, scope, read_contract_output, call_contract_function, send_amount)

# Integer arithmetic expression
class IntAexp(Aexp):
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return 'IntAexp(%d)' % self.i

    def eval(self, env, scope_map, scope, read_contract_output, call_contract_function, send_amount):
        return self.i

# Float arithmetic expression
class FloatAexp(Aexp):
    def __init__(self, f):
        self.f = f

    def __repr__(self):
        return 'FloatAexp(%f)' % self.f

    def eval(self, env,scope_map, scope, read_contract_output, call_contract_function, send_amount):
        return self.f

# Integer arithmetic expression
class StringAexp(Aexp):
    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return 'StringAexp(%s)' % self.s

    def eval(self, env, scope_map, scope, read_contract_output, call_contract_function, send_amount):
        return self.s

# List expression returning list of elements
class ListAexp(Aexp):
    def __init__(self, l):
        self.l = l

    def __repr__(self):
        return 'ListAexp(%s)' % self.l

    def eval(self, env, scope_map, scope, read_contract_output, call_contract_function, send_amount):
        return self.l

# Map expression returning empty dictionary
class MapAexp(Aexp):
    def __init__(self, m):
        self.m = {}

    def __repr__(self):
        return 'MapAexp(%s)' % self.m

    def eval(self, env, scope_map, scope, read_contract_output, call_contract_function, send_amount):
        return self.m

# Variable arithmetic expression
class VarAexp(Aexp):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'VarAexp(%s)' % self.name

    def eval(self, env, scope_map, scope, read_contract_output, call_contract_function, send_amount):
        if self.name in env:
            return env[self.name]
            # Here I am returning only the value of variable and not its scope
        else:
            raise NameError('name ' + self.name + ' is not defined in this scope')

# Function name expression
class FuncAexp(Aexp):
    def __init__(self, func):
        self.name = func[0]
        self.params = func[1]

    def __repr__(self):
        return 'FuncAexp(%s, %s)' % (self.name, str(self.params))

    def eval(self, env, scope_map, scope, read_contract_output, call_contract_function, send_amount):
        if self.name == "read_contract_output":
            self.params = check(self.params, env)
            return read_contract_output(self.params[0])
        elif self.name == "call_contract_function":
            self.params = check(self.params, env)
            return call_contract_function(self.params[0], self.params[1], self.params[2])
        elif self.name == "send_amount":
            self.params = check(self.params, env)
            return send_amount(self.params[0], self.params[1], self.params[2])
        elif self.name == "print":
            self.params = check(self.params, env)
            print(*self.params)
        elif self.name == "get_time":
            return time.time()
        elif self.name in env:
            new_env = {}
            new_scope_map = {}

            for name in env:
                if isinstance(env[name], Routine):
                    if self.name == name:
                        for i in range(len(env[name].params)):
                            if type(self.params[i]) == list:
                                new_env[env[name].params[i]] = env[self.params[i][0]]
                            else:
                                new_env[env[name].params[i]] = self.params[i]

                            if scope in new_scope_map:
                                new_scope_map[scope].append(env[name].params[i])
                            else:
                                new_scope_map[scope] = []
                                new_scope_map[scope].append(env[name].params[i])

                    new_env[name] = env[name]
                    if scope in new_scope_map:
                        new_scope_map[scope].append(name)
                    else:
                        new_scope_map[scope] = []
                        new_scope_map[scope].append(name)

            x = env[self.name].body.eval(new_env, new_scope_map, scope, read_contract_output, call_contract_function, send_amount)
            if x != None:
                return x

        else:
            raise NameError("No function found")

# Null expression
class NullAexp(Aexp):
    def __init__(self, n):
        self.n = n

    def __repr__(self):
        return 'NullAexp(%s)' % self.n

    def eval(self, env, scope_map, scope, read_contract_output, call_contract_function, send_amount):
        return None

# Indexing expression for any iterable
class IndexAexp(Aexp):
    def __init__(self, index_str):
        self.name = index_str[:index_str.index('[')] # This represents the env variable
        self.i = index_str[index_str.index('[') + 1 : index_str.index(']')] #This represents the index value

    def __repr__(self):
        return 'IndexAexp(%s, %s)' % (self.name, self.i)

    def eval(self, env, scope_map, scope, read_contract_output, call_contract_function, send_amount):
        if self.name in env:
            if type(env[self.name]) == str or type(env[self.name]) == list:
                if self.i.isnumeric():
                    self.i = int(self.i)
                    if self.i >= 0 and self.i < len(env[self.name]):
                        return env[self.name][self.i]
                    else:
                        raise IndexError('Index is out of bounds!!')
                else:
                    if self.i in env:
                        if isinstance(env[self.i], int):
                            if env[self.i] >= 0 and env[self.i] < len(env[self.name]):
                                return env[self.name][env[self.i]]
                            else:
                                raise IndexError('Index is out of bounds!!')
                        else:
                            raise TypeError('indices must be integers')
                    else:
                        raise NameError('name ' + self.i + ' is not defined in this scope')
            elif type(env[self.name]) == dict:
                # For float as a index
                if '.' in self.i:
                    self.i = float(self.i)

                #For string as a index
                elif '\'' in self.i:
                    self.i = str(self.i[1:-1])

                #For int as index
                else:
                    if self.i.isnumeric():
                        self.i = int(self.i)
                    else:
                        raise TypeError('Map keys must be either integers, float or string')
                
                if self.i in env[self.name].keys():
                    return env[self.name][self.i]
                else:
                    raise NameError('key : ' + str(self.i) + ' is not defined in this Map')
            else:
                raise RuntimeError('The identifier is not iterable!!!')
        else:
            raise NameError('name ' + self.name + ' is not defined in this scope')

# Binary operation arithmetic expresssion
class BinopAexp(Aexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return 'BinopAexp(%s, %s, %s)' % (self.op, self.left, self.right)

    def eval(self, env, scope_map, scope, read_contract_output, call_contract_function, send_amount):
        left_value = self.left.eval(env, scope_map, scope, read_contract_output, call_contract_function, send_amount)
        right_value = self.right.eval(env, scope_map, scope, read_contract_output, call_contract_function, send_amount)
        if self.op == '+':
            value = left_value + right_value
        elif self.op == '-':
            value = left_value - right_value
        elif self.op == '*':
            value = left_value * right_value
        elif self.op == '/':
            value = left_value / right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value

# Relational operation boolean expression
class RelopBexp(Bexp):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        return 'RelopBexp(%s, %s, %s)' % (self.op, self.left, self.right)

    def eval(self, env, scope_map, scope, read_contract_output, call_contract_function, send_amount):
        left_value = self.left.eval(env, scope_map, scope, read_contract_output, call_contract_function, send_amount)
        right_value = self.right.eval(env, scope_map, scope, read_contract_output, call_contract_function, send_amount)
        if self.op == '<':
            value = left_value < right_value
        elif self.op == '<=':
            value = left_value <= right_value
        elif self.op == '>':
            value = left_value > right_value
        elif self.op == '>=':
            value = left_value >= right_value
        elif self.op == '=':
            value = left_value == right_value
        elif self.op == '!=':
            value = left_value != right_value
        else:
            raise RuntimeError('unknown operator: ' + self.op)
        return value

# AND operation boolean expression
class AndBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'AndBexp(%s, %s)' % (self.left, self.right)

    def eval(self, env, scope_map, scope, read_contract_output, call_contract_function, send_amount):
        left_value = self.left.eval(env, scope_map, scope, read_contract_output, call_contract_function, send_amount)
        right_value = self.right.eval(env, scope_map, scope, read_contract_output, call_contract_function, send_amount)
        return left_value and right_value

# OR operation boolean expression
class OrBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'OrBexp(%s, %s)' % (self.left, self.right)

    def eval(self, env, scope_map, scope, read_contract_output, call_contract_function, send_amount):
        left_value = self.left.eval(env, scope_map, scope, read_contract_output, call_contract_function, send_amount)
        right_value = self.right.eval(env, scope_map, scope, read_contract_output, call_contract_function, send_amount)
        return left_value or right_value

# NOT operation boolean expression
class NotBexp(Bexp):
    def __init__(self, exp):
        self.exp = exp

    def __repr__(self):
        return 'NotBexp(%s)' % self.exp

    def eval(self, env, scope_map, scope, read_contract_output, call_contract_function, send_amount):
        value = self.exp.eval(env, scope_map, scope, read_contract_output, call_contract_function, send_amount)
        return not value
