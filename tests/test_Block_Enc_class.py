from enc import *
from testing_utils import *
from unittest import TestCase, main



class TestBlockClass(TestCase):

    def setUp(self) -> None:
        self.key = "test_key_123_11"
        self.hash = Keys.convert_to_hash(self.key)
        self.dict1, self.dict2 = Dict_Tools.get_dicts(self.key)
        self.txt = "qwertyuiopasdfghjklzxcvbnm"
        self.block = b(self.txt)
        

    def test_split_to_parts(self):
        for i in range(1,len(self.txt)):
            blocks = Block_Tools.split_to_parts(self.txt,i)
            blocks_txt = [block.bytes for block in blocks]

            self.assertTrue(same_but_splited(self.txt,blocks_txt))


    def test_connect_blocks(self):
        for i in range(1,len(self.txt)):
            blocks = Block_Tools.split_to_parts(self.txt,i)

            connected_txt = Block_Tools.connect_blocks(blocks)
            connected_txt = remove_modulo(connected_txt)
            
            self.assertEqual(self.txt,connected_txt)

    def test_xor_str_success(self):
        test_cases = [
                ("abcd","qwer"),
                ('123456789','987654321'),
                ('x','z'),
                ('h14823h','0hmdqt7')
    
        ]
        
        for text,key  in test_cases:
            block = b(text)
            String_tools.xor_str(block,key,self.dict1,self.dict2)
            
            result_is_different = block.bytes != text and block.bytes != key
            self.assertTrue(result_is_different)

            String_tools.xor_str(block,key,self.dict1,self.dict2)
            self.assertEqual(block.bytes,text)


    def test_xor_str_failure(self):
        test_cases = [
                ("abasdcd","qwer"),
                ('1234567a89fafasfsaf','987654asdas321'),
                ('x',''),
                ('h14g823hsadd','0hmdqt7'),
    
        ]       

        for txt,key in test_cases:
            try:
                String_tools.xor_str(b(txt),key,self.dict1,self.dict2)
                self.assertTrue(False)

            except Exception as excp:
                self.assertEqual(type(excp),ValueError)
                self.assertEqual(excp.args[0],'Text and key should be the same length in xor_str')

    def test_xor_block(self):
        for i in range(1,3):
            _,key_list = Keys.create_hash_list(self.hash, len(self.txt) +((len(self.txt) % i) - i ))
            key_list = list(''.join(key_list))
            key_list = ["".join(key_list[idx * i : (idx +1) * i]) for idx in range(len(key_list) // i)]
            
            blocks = Block_Tools.split_to_parts(self.txt,i)
            blocks_copy = copy_blocks(blocks)
            Block_Tools.xor_blocks(blocks_copy,key_list,self.dict1,self.dict2)

            for idx in range(len(blocks)):
                key = key_list[idx]
                xored_block = blocks_copy[idx]
                block = blocks[idx]

                self.assertEqual(block.bytes,String_tools.xor_str(xored_block,key,self.dict1,self.dict2))

            


    def test_mix_blocks(self):
        # adding more cases would take much time
        for i in range(1,3):
            un_joind,key_list = Keys.create_hash_list(self.hash, len(self.txt) +((len(self.txt) % i) - i ))
            key_list = list(''.join(key_list))
            key_list = ["".join(key_list[idx * i : (idx +1) * i]) for idx in range(len(key_list) // i)]
            
            blocks = Block_Tools.split_to_parts(self.txt,i)
            mixed_blocks = Block_Tools.mix_blocks(blocks,key_list)

            self.assertTrue(same_but_mixed(blocks,mixed_blocks))


    def test_un_mix_blocks(self):
        # adding more cases would take much time
        for i in range(1,3):
            un_joind , key_list= Keys.create_hash_list(self.hash, len(self.txt) +((len(self.txt) % i) - i ))
            key_list = list(''.join(key_list))
            key_list = ["".join(key_list[idx * i : (idx +1) * i]) for idx in range(len(key_list) // i)]
            
            blocks = Block_Tools.split_to_parts(self.txt,i)
            mixed_blocks = Block_Tools.mix_blocks(blocks,key_list)

            self.assertEqual(blocks,Block_Tools.un_mix_blocks(mixed_blocks,key_list))

    def test_string_shift(self):
        test_cases = [
                ('abcd',2,'cdab'),
                ('123456789',4,'678912345'),
                ('hola_myamigo',19,'myamigohola_'),
                ('',3,'')
        ]

        for txt,shift,result in test_cases:
            self.assertEqual(String_tools.string_shift(txt,shift),result)
    
    def test_string_un_shift(self):
        test_cases = [
                ('abcasd adssad',5),
                ('1234561010789',3),
                ('hola_myam123igo',19),
                ('',3)
        ]

        for txt,shift in test_cases:
            result = String_tools.string_shift(txt,shift)
            self.assertEqual(String_tools.string_un_shift(result,shift),txt)

    def test_string_bit_shift(self):
        test_cases_success = [
                ('abcasd adssad',5),
                ('1234561010789',3),
                ('hola_myam123igo',19),
                ('',3),
                ("mamamia gola tensioni",100)
        ]
        test_cases_error = [
                    (123442,124),
                    ('12345','as'),
                    (1234,'ds')
        ]

        for txt,shift in test_cases_success:
            result = String_tools.string_bit_shift(txt,self.dict1,self.dict2,shift)
            if result != "":
                self.assertNotEqual(result,txt)
            self.assertEqual(String_tools.string_bit_shift(result,self.dict1,self.dict2,shift,False),txt)

        for txt,shift in test_cases_error:
            try:
                String_tools.string_bit_shift(txt,self.dict1,self.dict2,shift)
                self.assertTrue(False)

            except Exception as excp :
                self.assertRaises(TypeError,type(excp))
                self.assertEqual(excp.args[0],"String should be str  and shiftnum should be int")
                
                
if __name__ == "__main__":
    main()