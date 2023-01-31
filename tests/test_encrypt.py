from testing_utils import *
from enc import AE as ae
import unittest


class TestEncrypt(unittest.TestCase):

    def setUp(self) -> None:
        self.test_cases = [
                    ('Lorem here and lorem there lorem lorem everywhere ' * 9,"my_password_123"),
                    ("123567", 'lt77ma@345'),
                    ('123456789','123456789'),
                    ('aaaa' * 100,"my_pass_is_my_pass@123")
                    ('The quick brown fox jumps over the lazy dog'* 2, 'mypassword1234'),
                    ('Hello World!' * 8, 'Hello_World_123'),
                    ('It is raining cats and dogs' * 9, 'rainyday123'),
                    ('There is no place like home' * 5, 'home12345'),
                    ('Once upon a time'* 7, 'onceuponatime1')
                    ('The sun rises in the east and sets in the west', 'sUnR1sEs_In_tHe_EaSt@west'),
                    ('All roads lead to Rome', 'rOmE_rOaD$_2022'),
                    ('A picture is worth a thousand words', 'p1cTurE_w0rd5_2023'),
                    ('An apple a day keeps the doctor away', 'aPple_d0cTor_awAy#'),
                    ('Where there is smoke, there is fire', 'sm0kE_fIrE_123')
                    ('The early bird catches the worm, but the second mouse gets the cheese', 'eArLy_b1rd_wrm_sEcndMousE_chEese'),
                    ('You can lead a horse to water, but you can’t make it drink', 'h0rsE_wAtEr_dr1nk_2022'),
                    ('Practice makes perfect', 'prActice_pErfEct_123'),
                    ('Rome was not built in a day', 'rOme_bu1lt_day_2023'),
                    ('Time heals all wounds', 't1me_hEals_w0unds_2021')
        ]

    def test_Encrypt(self):
        for txt, key in self.test_cases:
            encrypted = ae.Encrypt(txt,key)
            print(encrypted)
            self.assertNotEqual(encrypted, txt)

    def test_Decrypt(self):
        for txt, key in self.test_cases:
            encrypted = ae.Encrypt(txt,key)
            decrypted = ae.Decrypt(encrypted,key)
            print(decrypted)
            self.assertEqual(decrypted, txt)


