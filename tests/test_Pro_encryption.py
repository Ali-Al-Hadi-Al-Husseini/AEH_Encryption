from enc import AE as ae
import unittest


class TestProEncryption(unittest.TestCase):
    def setUp(self) -> None:
        self.test_cases = [
                    ('Lorem here and lorem there lorem lorem everywhere ' * 9,"my_password_123" * 9,3),
                    ("123567     " * 18 , 'lt77ma@345'*10,17),
                    ('123456789' * 27,'123456789'*10,5),
                    ('aaaa' * 100,"my_pass_is_my_pass@123" * 7,2)
        ]
        self.test_case_fail = [
                    ('Lorem here and lorem there lorem lorem everywhere ' * 9,"my_password_123",3),
                    ("123567", 'lt77ma@345',17),
                    ('123456789','123456789',5),
                    ('aaaa' * 100,"my_pass_is_my_pass@123",2)
        ]
        self.test_case_fail_decrypt = [
                    ('Lorem here and lorem there lorem lorem everywhere ' * 9,"my_password_123",64),
                    ("123567", 'lt77ma@345',17),
                    ('123456789','123456789',-1),
                    ('aaaa' * 100,"my_pass_is_my_pass@123",200)
        ]

    def test_professional_encryption(self):
        for txt,key,add in self.test_cases:
            encoded, chars = ae.professional_encryption(txt,key,add)
            self.test_chars = chars
            self.assertNotEqual(encoded,txt)

        for txt,key,add in self.test_case_fail:
            self.assertRaises(ValueError,lambda: ae.professional_encryption(txt,key,add))
            self.assertRaises(ValueError,lambda: ae.professional_encryption(txt,key * 10,len(key) * 10))

    def test_professional_decryption(self):
        chars_list = []
        for txt,key,add in self.test_cases:
            encoded, chars_list = ae.professional_encryption(txt,key,add)
            decoded =  ae.professional_decryption(encoded,key,add,chars_list)
            self.assertEqual(txt,decoded)

        for txt,key,add in self.test_case_fail_decrypt:
            self.assertRaises(ValueError,lambda: ae.professional_decryption(txt,key,add,chars_list))
            self.assertRaises(ValueError,lambda: ae.professional_decryption(txt,key * 10,len(key) * 10,chars_list))

if __name__ == '__main__':
    unittest.main()