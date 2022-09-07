from ..Enc.AEH import  AE as ae
import unittest



class TestBlockEncryption(unittest.TestCase):

    def setUp(self) -> None:
        self.test_cases = [
                    ('Lorem here and lorem there lorem lorem everywhere ' * 9,"my_password_123",3),
                    ("123567", 'lt77ma@345',5),
                    ('1234567 sfdsfsdfdsf sdfsdf ds89','123456789',9),
                    ('aaaa' * 100,"my_pass_is_my_pass@123",7)
        ]

    def test_block_encryption(self):
        for txt,key,rounds  in self.test_cases:
            encrypted = ae.block_encryption_rounds(txt,key,rounds)
            self.assertEqual(len(encrypted) % 64,0)
            self.assertNotEqual(encrypted,txt)


    def test_block_decryption(self):
        for txt,key,rounds in self.test_cases:
            encrypted = ae.block_encryption_rounds(txt,key,rounds)
            decoded = ae.block_decryption_rounds(encrypted,key,rounds)
            self.assertEqual(decoded,txt)