# Tokens regular expressions
from .lexer import *

RESERVED = 'RESERVED'
INT      = 'INT'
ID       = 'ID'

token_exprs = [
    (r'\n',                    None),
    (r'[ \t]+',                None),
    # (r'#[^\n]*',               None),
    (r'\:=',                   RESERVED),
    (r'\(',                    RESERVED),
    (r'\)',                    RESERVED),
    (r';',                     RESERVED),
    (r'\+',                    RESERVED),
    (r'-',                     RESERVED),
    (r'/\*',                   RESERVED),
    (r'\*/',                   RESERVED),
    (r'\*',                    RESERVED),
    (r'//',                    RESERVED),
    (r'/',                     RESERVED),
    (r'<=',                    RESERVED),
    (r'<',                     RESERVED),
    (r'>=',                    RESERVED),
    (r'>',                     RESERVED),
    (r'!=',                    RESERVED),
    (r'=',                     RESERVED),
    (r'[0-9]+',                INT),
    (r'[A-Za-z][A-Za-z0-9_]*', ID),
]

reserved_keywords = ['and', 'or', 'not', 'if', 'then', 'else', 'while', 'do', 'end']
comment_tokens = ['//', '/*', '*/']

def rig_lex(characters):
    return lex(characters, token_exprs, reserved_keywords, RESERVED)
