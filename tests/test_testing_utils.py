from .testing_utils import *
from ..Enc.enc import Block as b
import unittest





class TestTestingUtils(unittest.TestCase):
    
    def test_same_but_splited(self):
        test_cases_success = [
                ("qwertyuiopasdfghjklzxcvbnm",['qwer', 'tyui', 'opas', 'dfgh', 'jklz', 'xcvb', 'nm']),
                ('123',['123']),
                ('lilo_test_774',['li','lo_test','_774']),
                ('1234567890',['1234','5678','90']),
                ('asdfghjkl',['asd','fgh','jkl'])
        ]

        test_cases_failed = [
                ('1234',['1','2','3']),
                ('lkjhgfdsa',['lkj','hffdsa'])
        ]
        
        for txt, _list in test_cases_success:
            self.assertTrue(same_but_splited(txt,_list))

        for txt, _list in test_cases_failed:
            self.assertFalse(same_but_splited('1234',['1','2','3']))


    def test_remove_modulo(self):
        test_cases = [
                ('123','123%%%%%'),
                ('abfdfsad','abfdfsad%%%%%%%%%%%%%'),
                ('','%%%%%%%%%%%%%%%')
        ]

        for txt1,txt2 in test_cases:
            self.assertEqual(txt1,remove_modulo(txt2))

    def test_same_but_mixed_success(self):
        b1, b2 = b('123'),b('abc')
        test_cases = [
                (list('abcd'),list('cadb')),
                ([1,2,3,4],[4,1,3,2]),
                ([b1,b2],[b2,b1])
        ]

        for un_mixed,mixed in test_cases:
            self.assertTrue(same_but_mixed(un_mixed,mixed))

    def test_same_but_mixed_fail(self):
        b1, b2 = b('123'),b('abc')
        test_cases = [
                (list('abcd'),list('caadb')),
                ([1,2,3,4],[4,1,2,3,2]),
                ([b1,b2],[b2,b('asdsa')])
        ]

        for un_mixed,mixed in test_cases:
            self.assertFalse(same_but_mixed(un_mixed,mixed))