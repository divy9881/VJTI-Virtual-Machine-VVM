from .equality import *

class Statement(Equality):
    pass

class Aexp(Equality):
    pass

class Bexp(Equality):
    pass

# Assignment statement
class AssignStatement(Statement):
    def __init__(self, name, aexp):
        self.name = name
        self.aexp = aexp

    def __repr__(self):
        return 'AssignStatement(%s, %s)' % (self.name, self.aexp)

    def eval(self, env, scope):
        value = self.aexp.eval(env, scope)
        # Here if the name exists then we only change the value and no the scope
        # If not present we create a new entry
        if self.name in env:
            env[self.name][0] = value
        else:
            env[self.name] = list((value, scope))

# Compound statement
class CompoundStatement(Statement):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return 'CompoundStatement(%s, %s)' % (self.first, self.second)

    def eval(self, env, scope):
        self.first.eval(env, scope)
        self.second.eval(env, scope)

# If statement
class IfStatement(Statement):
    def __init__(self, condition, true_stmt, false_stmt):
        self.condition = condition
        self.true_stmt = true_stmt
        self.false_stmt = false_stmt

    def __repr__(self):
        return 'IfStatement(%s, %s, %s)' % (self.condition, self.true_stmt, self.false_stmt)

    def eval(self, env, scope):
        condition_value = self.condition.eval(env, scope)
        if condition_value:
            self.true_stmt.eval(env, scope + 1)
        else:
            if self.false_stmt:
                self.false_stmt.eval(env, scope + 1)
        
        # This loop add names of variable that were declared in if statement
        names_to_be_removed = []
        for name in env:
            if env[name][1] > scope:
                names_to_be_removed.append(name)
        
        # This loop removes the names from env
        for name in names_to_be_removed:
            env.pop(name)

# While Statement
class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'WhileStatement(%s, %s)' % (self.condition, self.body)

    def eval(self, env, scope):
        condition_value = self.condition.eval(env, scope)
        while condition_value:
            self.body.eval(env, scope + 1)
            condition_value = self.condition.eval(env, scope)

        # This loop add names of variable that were declared in while statement
        names_to_be_removed = []
        for name in env:
            if env[name][1] > scope:
                names_to_be_removed.append(name)
        
        # This loop removes the names from env
        for name in names_to_be_removed:
            env.pop(name)        

# Integer arithmetic expression
class IntAexp(Aexp):
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return 'IntAexp(%d)' % self.i

    def eval(self, env, scope):
        return self.i

# Float arithmetic expression
class FloatAexp(Aexp):
    def __init__(self, f):
        self.f = f

    def __repr__(self):
        return 'FloatAexp(%f)' % self.f

    def eval(self, env, scope):
        return self.f

# Integer arithmetic expression
class StringAexp(Aexp):
    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return 'StringAexp(%s)' % self.s

    def eval(self, env, scope):
        return self.s

# List expression returning list of elements
class ListAexp(Aexp):
    def __init__(self, l):
        self.l = l

    def __repr__(self):
        return 'ListAexp(%s)' % self.l

    def eval(self, env, scope):
        return self.l

# Map expression returning empty dictionary
class MapAexp(Aexp):
    def __init__(self, m):
        self.m = {}

    def __repr__(self):
        return 'MapAexp(%s)' % self.m

    def eval(self, env, scope):
        return self.m

# Variable arithmetic expression
class VarAexp(Aexp):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'VarAexp(%s)' % self.name

    def eval(self, env, scope):
        if self.name in env:
            return env[self.name][0]
            # Here I am returning only the value of variable and not its scope
        else:
            raise NameError('name ' + self.name + ' is not defined in this scope')

# Indexing expression for any iterable
class IndexAexp(Aexp):
    def __init__(self, index_str):
        self.name = index_str[:index_str.index('[')] # This represents the env variable
        self.i = index_str[index_str.index('[') + 1 : index_str.index(']')] #This represents the index value

    def __repr__(self):
        return 'IndexAexp(%s, %s)' % (self.name, self.i)

    def eval(self, env, scope):
        if self.name in env:
            if type(env[self.name][0]) == str or type(env[self.name][0]) == list:
                if self.i.isnumeric():
                    self.i = int(self.i)
                    if self.i >= 0 and self.i < len(env[self.name][0]):
                        return env[self.name][0][self.i]
                    else:
                        raise IndexError('Index is out of bounds!!')
                else:
                    if self.i in env:
                        if isinstance(env[self.i][0], int):
                            if env[self.i][0] >= 0 and env[self.i][0] < len(env[self.name][0]):
                                return env[self.name][0][env[self.i][0]]
                            else:
                                raise IndexError('Index is out of bounds!!')
                        else:
                            raise TypeError('indices must be integers')
                    else:
                        raise NameError('name ' + self.i + ' is not defined in this scope')
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

    def eval(self, env, scope):
        left_value = self.left.eval(env, scope)
        right_value = self.right.eval(env, scope)
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

    def eval(self, env, scope):
        left_value = self.left.eval(env, scope)
        right_value = self.right.eval(env, scope)
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

    def eval(self, env, scope):
        left_value = self.left.eval(env, scope)
        right_value = self.right.eval(env, scope)
        return left_value and right_value

# OR operation boolean expression
class OrBexp(Bexp):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return 'OrBexp(%s, %s)' % (self.left, self.right)

    def eval(self, env, scope):
        left_value = self.left.eval(env, scope)
        right_value = self.right.eval(env, scope)
        return left_value or right_value

# NOT operation boolean expression
class NotBexp(Bexp):
    def __init__(self, exp):
        self.exp = exp

    def __repr__(self):
        return 'NotBexp(%s)' % self.exp

    def eval(self, env, scope):
        value = self.exp.eval(env, scope)
        return not value
