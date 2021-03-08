# Tokens regular expressions
from .lexer import *

RESERVED = 'RESERVED'
INT      = 'INT'
ID       = 'ID'
FLOAT    = 'FLOAT'
STRING   = 'STRING'
INDEX    = 'INDEX'
LIST     = 'LIST'
MAP      = 'MAP'
FUNC     = 'FUNC'
NULL     = 'NULL'

token_exprs = [
    (r'\n',                                            None),
    (r'[ \t]+',                                        None),
    # (r'#[^\n]*',                                     None),
    (r'\:=',                                           RESERVED),
    (r'\(',                                            RESERVED),
    (r'\)',                                            RESERVED),
    (r';',                                             RESERVED),
    (r'\+',                                            RESERVED),
    (r'-',                                             RESERVED),
    (r'/\*',                                           RESERVED),
    (r'\*/',                                           RESERVED),
    (r'\*',                                            RESERVED),
    (r'//',                                            RESERVED),
    (r'/',                                             RESERVED),
    (r'<=',                                            RESERVED),
    (r'<',                                             RESERVED),
    (r'>=',                                            RESERVED),
    (r'>',                                             RESERVED),
    (r'!=',                                            RESERVED),
    (r'=',                                             RESERVED),
    (r'[A-Za-z][A-Za-z0-9_]*\[[A-Za-z0-9_.\']+\]',     INDEX),
    (r'\[',                                            RESERVED),
    (r'\,',                                            RESERVED),
    (r'\]',                                            RESERVED),
    (r'{}',                                            MAP),
    (r'\'[A-Za-z][A-Za-z]*\'',                         STRING),
    (r'[0-9]+\.[0-9]+',                                FLOAT),
    (r'[0-9]+',                                        INT),
    (r'null',                                          NULL),
    (r'[A-Za-z][A-Za-z0-9_]*',                         ID),
]

reserved_keywords = ['and', 'or', 'not', 'if', 'then', 'else', 'while', 'do', 'end', 'function', 'return']
comment_tokens = ['//', '/*', '*/']
list_tokens = ['[', ']']
function_tokens = ['(', ')']

def rig_lex(characters):
    return lex(characters, token_exprs, reserved_keywords, RESERVED)
