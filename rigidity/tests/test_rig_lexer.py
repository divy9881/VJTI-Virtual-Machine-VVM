import unittest
from ..rigidity_lexer import *
from ..rigidity_parser import *

class TestLexer(unittest.TestCase):
    def lexer_test(self, code, expected):
        actual = lex(code, token_exprs, reserved_keywords, RESERVED)
        self.assertEqual(expected, actual)

    def test_empty(self):
        self.lexer_test('', [])

    def test_id(self):
        self.lexer_test('abc', [['abc', ID]])

    def test_keyword_1(self):
        self.lexer_test('while', [['while', RESERVED]])
    
    def test_keyword_2(self):
        self.lexer_test('whilet dot if', [['whilet', ID], ['dot', ID], ['if', RESERVED]])

    def test_space(self):
        self.lexer_test(' ', [])

    def test_id_space(self):
        self.lexer_test('abc def', [['abc', ID], ['def', ID]])
