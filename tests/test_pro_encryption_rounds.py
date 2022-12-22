from Enc import AE as ae
from unittest import TestCase


class TestProEncryption(TestCase):
    def setUp(self) -> None:
        self.test_cases = [
                    ('Lorem here and lorem there lorem lorem everywhere ' * 9,"my_password_123" * 9,3,2),
                    ("123567@mansad" * 18 , 'lt77ma@453'*10,1,4),
                    ('123456789' * 27,'123456789'*10,5,6),
                    ('aaaa' * 100,"my_pass_is_my_pass@123" * 7,2,1)
        ]
        self.test_case_fail = [
                    ('Lorem here and lorem there lorem lorem everywhere ' * 9,"my_password_123",3,3),
                    ("123567", 'lt77ma@345',17,9),
                    ('123456789','123456789',5,7),
                    ('aaaa' * 100,"my_pass_is_my_pass@123",2,4)
        ]
        self.test_case_fail_decrypt = [
                    ('Lorem here and lorem there lorem lorem everywhere ' * 9,"my_password_123",-1,10),
                    ("123567", 'lt77ma@345',17,9),
                    ('123456789','123456789',-1,8),
                    ('aaaa' * 100,"my_pass_is_my_pass@123",200,200)
        ]

    def test_professional_block_encryption_rounds(self):
        for txt,key,add,rounds in self.test_cases:
            encoded, chars = ae.professional_block_encryption_rounds(txt,key,add,rounds)
            self.test_chars = chars
            self.assertNotEqual(encoded,txt)

        for txt,key,add,rounds in self.test_case_fail:
            self.assertRaises(ValueError,lambda: ae.professional_block_encryption_rounds(txt,key,add,rounds))
            self.assertRaises(ValueError,lambda: ae.professional_block_encryption_rounds(txt,key * 10,len(key) * 10,rounds))

    def test_professional_block_decryption_rounds(self):
        chars_list = []
        for txt,key,add,rounds in self.test_cases:
            encoded, chars_list = ae.professional_block_encryption_rounds(txt,key,add,rounds)
            decoded =  ae.professional_block_decryption_rounds(encoded,key,add,chars_list,rounds)
            self.assertEqual(txt,decoded)

        for txt,key,add,rounds in self.test_case_fail_decrypt:
            print("???????????????????????????????????????????/")
            print(key)
            self.assertRaises(ValueError,lambda: ae.professional_block_decryption_rounds (txt,key,add,chars_list,rounds))
            self.assertRaises(ValueError,lambda: ae.professional_block_decryption_rounds(txt,key * 10,len(key) * 10,chars_list))

