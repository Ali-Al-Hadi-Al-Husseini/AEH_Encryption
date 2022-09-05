from ..Enc.AEH import  AE as ae
import unittest



class TestEncryptShuffling(unittest.TestCase):

    def setUp(self) -> None:
        self.test_cases = [
                    ('Lorem here and lorem there lorem lorem everywhere ' * 9,"my_password_123"),
                    ("123567", 'lt77ma@345'),
                    ('123456789','123456789'),
                    ('aaaa' * 100,"my_pass_is_my_pass@123")
        ]

    def test_Encrypt(self):
        for txt, key in self.test_cases:
            encrypted = ae.Encrypt_with_shuffling(txt,key)
            self.assertNotEqual(encrypted, txt)

    def test_Decrypt(self):
        for txt, key in self.test_cases:
            encrypted = ae.Encrypt_with_shuffling(txt,key)
            decrypted = ae.Decrypt_with_shuffling(encrypted,key)
            self.assertEqual(decrypted, txt)