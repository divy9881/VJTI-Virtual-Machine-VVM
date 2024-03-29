# Token parsers
from ..combinators import *
from ..rig_ast import *
from ..rigidity_lexer import *
from functools import reduce
    
# Basic parsers
def keyword(kw):
    return Reserved(kw, RESERVED)

num_i = Tag(INT) ^ (lambda i: int(i))
num_f = Tag(FLOAT) ^ (lambda f: float(f))
num_s = Tag(STRING) ^ (lambda s: str(s))
id = Tag(ID)
index = Tag(INDEX)
new_list = Tag(LIST)
new_map = Tag(MAP)
new_func = Tag(FUNC)
nil = Tag(NULL)

# Top level parser
def rig_parse(tokens):
    ast = parser()(tokens, 0)
    # Here parser function returs a Phrase object to which tokens and zero is passed 
    # and __call__ of Phrase is called.
    return ast

def parser():
    return Phrase(stmt_list())
    # Here stmt_list() returns a parser

# Statements
def stmt_list():
    separator = keyword(';') ^ (lambda x: lambda l, r: CompoundStatement(l, r))
    # This returns a Process Object with the keyword function acting as parser
    return Exp(stmt(), separator)
    # Here stmt() acts as the parser

def stmt():
    return assign_stmt() | \
           if_stmt()     | \
           while_stmt()  | \
           function_stmt() | \
           function_call_stmt() | \
           return_stmt()       

def assign_stmt():
    def process(parsed):
        ((name, _), exp) = parsed
        return AssignStatement(name, exp)
    return (id + keyword(':=') + aexp() ^ process) | \
           (index + keyword(':=') + aexp() ^ process)
    # Here + concats the results and ^ will create a process object
    # The `id + keyword(':=') + aexp()` is passed as parameter to the process function

def if_stmt():
    def process(parsed):
        (((((_, condition), _), true_stmt), false_parsed), _) = parsed
        if false_parsed:
            (_, false_stmt) = false_parsed
        else:
            false_stmt = None
        return IfStatement(condition, true_stmt, false_stmt)
    return (keyword('if') + bexp() + \
           keyword('then') + Lazy(stmt_list) + \
           Opt(keyword('else') + Lazy(stmt_list)) + \
           keyword('end') ^ process) | \
           (keyword('if') + aexp() + \
           keyword('then') + Lazy(stmt_list) + \
           Opt(keyword('else') + Lazy(stmt_list)) + \
           keyword('end') ^ process) 

def while_stmt():
    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return WhileStatement(condition, body)
    return keyword('while') + bexp() + \
           keyword('do') + Lazy(stmt_list) + \
           keyword('end') ^ process

def function_call_stmt():
    def process(parsed):
        (func) = parsed
        return FunctionCallStatement(func)
    return aexp() ^ process

def function_stmt():
    def process(parsed):
        ((((_, func), _), body), _) = parsed
        return FunctionStatement(func, body)
    return keyword('function') + aexp() + \
           keyword('do') + Lazy(stmt_list) + \
           keyword('end') ^ process

def return_stmt():
    def process(parsed):
        (_, name) = parsed
        return ReturnStatement(name)
    return keyword('return') + aexp() ^ process

# Boolean expressions
def bexp():
    return precedence(bexp_term(),
                      bexp_precedence_levels,
                      process_logic)

def bexp_term():
    return bexp_not()   | \
           bexp_relop() | \
           bexp_group()

def bexp_not():
    return keyword('not') + Lazy(bexp_term) ^ (lambda parsed: NotBexp(parsed[1]))

def bexp_relop():
    relops = ['<', '<=', '>', '>=', '=', '!=']
    return aexp() + any_operator_in_list(relops) + aexp() ^ process_relop

def bexp_group():
    return keyword('(') + Lazy(bexp) + keyword(')') ^ process_group

# Arithmetic expressions
def aexp():
    return precedence(aexp_term(),
                      aexp_precedence_levels,
                      process_binop)

def aexp_term():
    return aexp_value() | aexp_group()

def aexp_group():
    return keyword('(') + Lazy(aexp) + keyword(')') ^ process_group
           
def aexp_value():
    return (num_i ^ (lambda i: IntAexp(i))) | \
           (num_f ^ (lambda f: FloatAexp(f))) | \
           (num_s ^ (lambda s: StringAexp(s))) | \
           (id ^ (lambda v: VarAexp(v))) | \
           (index ^ (lambda i: IndexAexp(i))) | \
           (new_list ^ (lambda l: ListAexp(l))) | \
           (new_map ^ (lambda m: MapAexp(m))) | \
           (new_func ^ (lambda f: FuncAexp(f))) | \
           (nil ^ (lambda n: NullAexp(n)))

# An RIG-specific combinator for binary operator expressions (aexp and bexp)
def precedence(value_parser, precedence_levels, combine):
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine
    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser

# Miscellaneous functions for binary and relational operators
def process_binop(op):
    return lambda l, r: BinopAexp(op, l, r)

def process_relop(parsed):
    ((left, op), right) = parsed
    return RelopBexp(op, left, right)

def process_logic(op):
    if op == 'and':
        return lambda l, r: AndBexp(l, r)
    elif op == 'or':
        return lambda l, r: OrBexp(l, r)
    else:
        raise RuntimeError('unknown logic operator: ' + op)

def process_group(parsed):
    ((_, p), _) = parsed
    return p

def any_operator_in_list(ops):
    op_parsers = [keyword(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser

# Operator keywords and precedence levels
aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]

bexp_precedence_levels = [
    ['and'],
    ['or'],
]
