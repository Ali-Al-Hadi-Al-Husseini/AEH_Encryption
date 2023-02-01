from testing_utils import *
from enc import AE as ae
from enc import get_characters_list
import unittest


class TestEncrypt(unittest.TestCase):

    def setUp(self) -> None:
        self.len_char_list = len(get_characters_list())
        self.test_cases = [
                    ('Lorem here and lorem there lorem lorem everywhere ' * 9,"my_password_123"),
                    ("123567", 'lt77ma@345'),
                    ('123456789','123456789'),
                    ('aaaa' * 100,"my_pass_is_my_pass@123"),
                    ('The quick brown fox jumps over the lazy dog'* 2, 'mypassword1234'),
                    ('Hello World!' * 8, 'Hello_World_123'),
                    ('It is raining cats and dogs' * 9, 'rainyday123'),
                    ('There is no place like home' * 5, 'home12345'),
                    ('Once upon a time'* 7, 'onceuponatime1'),
                    ('The sun rises in the east and sets in the west', 'sUnR1sEs_In_tHe_EaSt@west'),
                    ('All roads lead to Rome', 'rOmE_rOaD$_2022'),
                    ('A picture is worth a thousand words', 'p1cTurE_w0rd5_2023'),
                    ('An apple a day keeps the doctor away', 'aPple_d0cTor_awAy#'),
                    ('Where there is smoke, there is fire', 'sm0kE_fIrE_123'),
                    ('The early bird catches the worm, but the second mouse gets the cheese', 'eArLy_b1rd_wrm_sEcndMousE_chEese'),
                    ('You can lead a horse to water, but you can’t make it drink', 'h0rsE_wAtEr_dr1nk_2022'),
                    ('Practice makes perfect' * 96, 'prActice_pErfEct_123'),
                    ('Rome was not built in a day' * 17, 'rOme_bu1lt_day_2023'),
                    ('Time heals all wounds'* 10, 't1me_hEals_w0unds_2021'),
                    ('Success is not final, failure is not fatal: it is the courage to continue that counts' * 2, 'sUcCess_fAilure_cOurage_c0ntinue'),
                    ('Every cloud has a silver lining' * 3, 'cl0ud_s1lverL1ning_2021'),
                    ('Actions speak louder than words'* 11, 'acti0ns_speak_w0rds_2023'),
                    ('Good things come to those who wait'* 3, 'g00d_th1ngs_wait_2022'),
                    ('Where there’s life, there’s hope', 'l1fe_h0pe_2023'),
                    ('Necessity is the mother of invention', 'necess1ty_m0ther_inventi0n_2022'),
                    ('A bird in the hand is worth two in the bush', 'b1rd_hand_tw0_bush_2021')                    
        ]

    def test_Encrypt(self):
        for txt, key in self.test_cases:
            txt *= 3
            encrypted = ae.Encrypt(txt,key)
            occurrences  = get_char_frequencies(encrypted).values()

            """Check if the difference between the most and least occurring number is less than 4% of the total number of letters."""
            self.assertTrue((max(occurrences) - min(occurrences)) <= sum(occurrences) * 0.04)
            
            self.assertEqual(len(encrypted)  , len(txt))
            self.assertNotEqual(encrypted, txt)

    def test_Decrypt(self):
        for txt, key in self.test_cases:
            encrypted = ae.Encrypt(txt,key)
            decrypted = ae.Decrypt(encrypted,key)
            self.assertEqual(decrypted, txt)

if __name__ == "__main__":
    unittest.main()

