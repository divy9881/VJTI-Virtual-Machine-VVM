import unittest
from ..rigidity_lexer import *
from ..rigidity_parser import *

class TestEvaluation(unittest.TestCase):
    def program_test(self, code, expected_env):
        tokens = rig_lex(code)
        optimized_tokens = optimize_tokens(tokens)
        result = rig_parse(optimized_tokens)
        self.assertNotEqual(None, result)
        program = result.value
        env = {}
        program.eval(env, 0)
        self.assertEqual(expected_env, env)

    def error_test(self, code, expected_error):
        tokens = rig_lex(code)
        optimized_tokens = optimize_tokens(tokens)
        result = rig_parse(optimized_tokens)
        self.assertNotEqual(None, result)
        program = result.value
        env = {}
        self.assertRaises(expected_error, lambda: program.eval(env, 0))

    def test_assign(self):
        self.program_test('x := 1', {'x': [1, 0]})

    def test_compound(self):
        self.program_test('x := 1; y := 2', {'x': [1, 0], 'y': [2, 0]})

    def test_if(self):
        self.program_test('if 1 < 2 then x := 1 else x := 2 end', {})

    def test_single_line_comment(self):
        self.program_test(
            '''
            x := 1;
            // y := 2;
            z := 3
            ''',
            {'x': [1, 0], 'z': [3, 0]}
        )

    def test_multi_line_comment(self):
        self.program_test(
            '''
            x := 1
            /*
            y := 2;
            z := 3
            */
            ''',
            {'x': [1, 0]}
        )

    def test_int_float_string(self):
        self.program_test(
            '''
            n := 5;
            factorial := 1.0;
            str := 'test'
            ''',
            {'n': [5, 0], 'factorial': [1.0, 0], 'str': ['test', 0]}
        )

    def test_indexing_int_string(self):
        self.program_test(
            '''
            str := 'test';
            s := str[0]
            ''',
            {'str': ['test', 0], 's': ['t', 0]}
        )

    def test_indexing_variable_string(self):
        self.program_test(
            '''
            n := 1;
            str := 'test';
            s := str[n]
            ''',
            {'n': [1, 0], 'str': ['test', 0], 's': ['e', 0]}
        )

    def test_list(self):
        self.program_test(
            '''
            n := [1,1.0, 'test'];
            ''',
            {'n': [[1,1.0,'test'], 0]}
        )

    def test_list_indexing(self):
        self.program_test(
            '''
            n := [1,2];
            a := n[0]
            ''',
            {'n': [[1,2], 0], 'a': [1, 0]}
        )                     

    def test_map(self):
        self.program_test(
            '''
            n := {};
            n[1] := 1;
            n[1.2] := 1.2;
            n['test'] := 'test'
            ''',
            {'n': [{1: 1, 1.2: 1.2, 'test': 'test'}, 0]}
        )     

    def test_map_indexing(self):
        self.program_test(
            '''
            n := {};
            n[1] := 1;
            n[1.2] := 1.2;
            n['test'] := 'test';
            a := n['test']
            ''',
            {'n': [{1: 1, 1.2: 1.2, 'test': 'test'}, 0], 'a': ['test', 0]}
        )         

    def test_scope_error(self):
        self.error_test(
            '''
            n := 5;
            factorial := 1;
            while n > 0 do
                factorial := factorial * n;
                n := n - 1;
                k := n + 1
            end;
            bot := k + 1
            ''',
            NameError
        )

    def test_index_out_of_bounds_error(self):
        self.error_test(
            '''
            str := 'test';
            s := str[5]
            ''',
            IndexError
        )

    def test_index_var_error(self):
        self.error_test(
            '''
            n := 0;
            str := 'test';
            s := str[t]
            ''',
            NameError
        )

    def test_index_string_error(self):
        self.error_test(
            '''
            str := 'test';
            s := st[0]
            ''',
            NameError
        )

    def test_index_error(self):
        self.error_test(
            '''
            n := 1.0;
            str := 'test';
            s := str[n]
            ''',
            TypeError
        )

    def test_index_runtime_error(self):
        self.error_test(
            '''
            n := 1.0;
            str := 'test';
            s := n[0]
            ''',
            RuntimeError
        )

    def test_map_invalid_key(self):
        self.error_test(
            '''
            n := {};
            n[1] := 1;
            n[1.2] := 1.2;
            n['test'] := 'test';
            a := n[2]
            ''',
            NameError
        )        

    # def test_while(self):
    #     self.program_test('x := 10; y := 0; while x > 0 do y := y + 1 end', {'x': 0, 'y': 10})
