import unittest
from ..rigidity_lexer import *
from ..rigidity_parser import *

class TestEvaluation(unittest.TestCase):
    def program_test(self, code, expected_env):
        tokens = rig_lex(code)
        result = rig_parse(tokens)
        self.assertNotEqual(None, result)
        program = result.value
        env = {}
        program.eval(env)
        self.assertEqual(expected_env, env)

    def test_assign(self):
        self.program_test('x := 1', {'x': 1})

    def test_compound(self):
        self.program_test('x := 1; y := 2', {'x': 1, 'y': 2})

    def test_if(self):
        self.program_test('if 1 < 2 then x := 1 else x := 2 end', {'x': 1})

    # def test_while(self):
    #     self.program_test('x := 10; y := 0; while x > 0 do y := y + 1 end', {'x': 0, 'y': 10})
