from enc import  Block
from unittest import TestCase


class TestBlockClass(TestCase):


    def setUp(self) -> None:
        self.txt = "qwertyuiopasdfghjklzxcvbnm"
        self.block = Block(self.txt)
        self.key = "test_key_123_11"


    def test_mix(self) -> None :
        self.block.mix(self.key)
        self.assertNotEqual(self.block.bytes,self.txt)
    
    def test_un_mix(self):
        old_txt = self.block.bytes

        self.block.mix(self.key)
        self.block.un_mix(self.key)

        self.assertEqual(old_txt,self.block.bytes)

    def test_len(self):
        self.assertEqual(len(self.txt),len(self.block))

