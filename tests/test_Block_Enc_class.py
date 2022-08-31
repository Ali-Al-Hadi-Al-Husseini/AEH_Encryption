from ..Enc.enc import  Block_Enc as be
from ..Enc.enc import Block as b
from ..Enc.enc import Enc as e
from .testing_utils import same_but_mixed, same_but_splited, remove_modulo
import unittest



class TestBlockClass(unittest.TestCase):

    def setUp(self) -> None:
        self.key = "test_key_123_11"
        self.hash = e.convert_to_hash(self.key)
        self.dict1, self.dict2 = e.get_dicts(self.key)
        self.txt = "qwertyuiopasdfghjklzxcvbnm"
        self.block = b(self.txt)
        

    def test_split_to_parts(self):
        for i in range(1,len(self.txt)):
            blocks = be.split_to_parts(self.txt,i)
            blocks_txt = [block.bytes for block in blocks]

            self.assertTrue(same_but_splited(self.txt,blocks_txt))


    def test_connect_blocks(self):
        for i in range(1,len(self.txt)):
            blocks = be.split_to_parts(self.txt,i)

            connected_txt = be.connect_blocks(blocks)
            connected_txt = remove_modulo(connected_txt)
            
            self.assertEqual(self.txt,connected_txt)

    def test_xor_str(self):
        test_cases = [
                ("abcd","qwer"),
                ('123456789','987654321'),
                ('x','z'),
                ('h14823h','0hmdqt7')
    
        ]
        
        for text,key  in test_cases:
            block = b(text)
            be.xor_str(block,key,self.dict1,self.dict2)
            
            result_is_different = block.bytes != text and block.bytes != key
            self.assertTrue(result_is_different)

            be.xor_str(block,key,self.dict1,self.dict2)
            self.assertEqual(block.bytes,text)

    def test_mix_blocks(self):
        # adding more cases would take much time
        for i in range(1,3):
            un_joind = e.create_hash_list(self.hash, len(self.txt) +((len(self.txt) % i) - i ))
            key_list = ["".join(un_joind[idx * i : (idx +1) * i]) for idx in range(len(un_joind) // i)]
            
            blocks = be.split_to_parts(self.txt,i)
            mixed_blocks = be.mix_blocks(blocks,key_list)

            self.assertTrue(same_but_mixed(blocks,mixed_blocks))


    def test_un_mix_blocks(self):
        # adding more cases would take much time
        for i in range(1,3):
            un_joind = e.create_hash_list(self.hash, len(self.txt) +((len(self.txt) % i) - i ))
            key_list = ["".join(un_joind[idx * i : (idx +1) * i]) for idx in range(len(un_joind) // i)]
            
            blocks = be.split_to_parts(self.txt,i)
            mixed_blocks = be.mix_blocks(blocks,key_list)

            self.assertEqual(blocks,be.un_mix_blocks(mixed_blocks,key_list))

        
