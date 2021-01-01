import sys
import unittest

if __name__ == '__main__':
    test_names = ['rigidity.tests.test_rig_lexer', 'rigidity.tests.test_combinators', 'rigidity.tests.test_rig_parser', 'rigidity.tests.test_eval']
    suite = unittest.defaultTestLoader.loadTestsFromNames(test_names)
    result = unittest.TextTestRunner().run(suite)
