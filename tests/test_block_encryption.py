from enc import  AE as ae
from unittest import TestCase

# from hypothesis import given, example,settings
# from hypothesis.strategies import text


class TestBlockEncryption(TestCase):

    def setUp(self) -> None:
        self.test_cases = [
                    ('Lorem here and lorem there lorem lorem everywhere ' * 9,"my_password_123"),
                    ("123567", 'lt77ma@345'),
                    ('1234567 sfdsfsdfdsf sdfsdf ds89','123456789'),
                    ('aaaa' * 100,"my_pass_is_my_pass@123")
        ]

    def test_block_encryption(self):
        for txt,key in self.test_cases:
            encrypted = ae.Block_Encryption(txt,key)
            self.assertEqual(len(encrypted) % 64,0)
            self.assertNotEqual(encrypted,txt)

    def test_block_decryption(self):
        for txt,key in self.test_cases:
            encrypted = ae.Block_Encryption(txt,key)
            self.assertEqual(ae.Block_Decryption(encrypted,key),txt)