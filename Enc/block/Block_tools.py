from ..Encryption_Tools.String_tools import String_tools
from ..Encryption_Tools.keys_tools import Keys
from ..Encryption_Tools.Dict_tools import Dict_Tools
from multiprocessing import Process

from numpy import empty
from typing import List, Dict

from ..Encryption_Tools.characters_list import  BITS_SIZE


class Block:
    def __init__(self,bytes: str) -> None:
        self.bytes = bytes

    def mix(self,key: str) -> None:
        self.bytes = Shuffle.shuffle_bin(self.bytes,key)


    def un_mix(self,key: str) -> None:
        self.bytes = Shuffle.un_shuffle_bin(self.bytes,key)
    
    def __len__(self) -> None:
        return len(self.bytes)

class Block_Tools:

    @classmethod
    def split_to_parts(cls, text: str, block_size: int = 16) -> List[Block]:
        blocks = []
        last_idx = 0

        for idx in range(len(text) // block_size):
            splitted_txt = text[idx * block_size : (idx + 1 ) * block_size]
            blocks.append(Block(splitted_txt))
            last_idx = idx

        txt =text[(last_idx + 1) * block_size:]

        if txt != '':
            last_block  = Block(txt)
            blocks.append(last_block)

        return blocks

    @classmethod
    def connect_blocks(cls, blocks: List[Block]) -> str:
        return ''.join([block.bytes for block in blocks])

    @classmethod
    def mix_blocks(cls, blocks: List[Block], key_list: List[str]) -> List[Block]:

        for idx  in range(len(blocks)):
            blocks[idx].mix(key_list[idx])

        return cls.mixblock(blocks,key_list[-1])


    @classmethod
    def un_mix_blocks(cls, blocks: List[Block], key_list: List[str]) -> List[Block]:
        blocks = cls.unmixblock(blocks,key_list[-1])

        for idx  in range(len(blocks)):
            blocks[idx].un_mix(key_list[idx])

        return blocks


    @classmethod
    def mixblock(cls,blocks: List[Block], key: str) -> List[Block]:
        row_shifts = Shuffle.generate_shuffle_list(len(blocks), len(blocks), key)
        aux_list = blocks[:]

        for idx in range(len(blocks)):
            aux_list[idx] = blocks[row_shifts[idx]]
        
        return aux_list


    @classmethod
    def unmixblock(cls,blocks: List[Block], key: str) -> List[Block]:
        row_shifts = Shuffle.generate_shuffle_list(len(blocks), len(blocks), key)

        aux_list = blocks[:]

        for idx in range(len(blocks)):
            aux_list[row_shifts[idx]] = blocks[idx] 

        return aux_list


    @classmethod
    def xor_blocks(cls,blocks: List[Block], key_list: List[Block], dict1: Dict[int,str], dict2: Dict[str,int]) -> None:

        for idx  in range(len(blocks)):
            String_tools.xor_str(blocks[idx],key_list[idx],dict1,dict2)



    @classmethod
    def mix_blocks_process(cls, blocks: List[Block], key_list: List[str]) -> List[Block]:
        processs = []
        for idx  in range(len(blocks)):
            process = Process(target=blocks[idx].mix,args=(key_list[idx],))
            process.start()
            processs.append(process)
        
        for process in processs:
            process.join()

        return cls.mixblock(blocks,key_list[-1])

    @classmethod
    def un_mix_blocks_process(cls, blocks: List[Block], key_list: List[str]) -> List[Block]:
        processs = []
        blocks = cls.unmixblock(blocks,key_list[-1])
        for idx  in range(len(blocks)):
            process = Process(target=blocks[idx].mix,args=(key_list[idx],))
            process.start()
            processs.append(process)
            

        for process in processs:
            process.join()

        return blocks

    @classmethod
    def xor_blocks_procsess(cls,blocks: List[Block], key_list: List[str], dict1,dict2) -> None: 
        processs = []
        for idx  in range(len(blocks)):
            process = Process(target=String_tools.xor_str,args=(blocks[idx],key_list[idx],dict1,dict2))
            process.start()
            processs.append(process)
            

        for process in processs:
            process.join()

class Shuffle:
    @classmethod
    def generate_shuffle_list(cls,len_txt,org_len,key):
        
        new_nums = []
        nums = []
        temp_num = list(range(org_len ))
        nums = Keys.generate_keylist(len_txt, key)

        for idx in range(org_len):
            new_idx = nums[idx] % (len(temp_num))
            new_nums.append(temp_num[new_idx])
            
            temp_num[-1], temp_num[new_idx] =  temp_num[new_idx], temp_num[-1]
            temp_num.pop()

        return new_nums

    @classmethod
    def list_shuffle(cls, array: List, key: str)-> List:
        new_array = [None for _ in array]
        row_shifts = cls.generate_shuffle_list(len(array) * 2 , len(array), key)

        for idx in range(len(array)):
            new_array[idx] = array[row_shifts[idx]]

        return new_array

    @classmethod
    def shuffle(cls, txt, key):
        new_txt = empty(len(txt),dtype='<U2')
        row_shifts = cls.generate_shuffle_list(len(txt) * 2 , len(txt), key)

        for idx in range(len(txt)):
            new_txt[idx] = txt[row_shifts[idx]]

        return ''.join(new_txt)


    @classmethod
    def un_shuffle(cls, txt, key):
        shifts = cls.generate_shuffle_list(len(txt) * 2, len(txt) , key)
        new_list = empty(len(txt),dtype='<U2')

        for idx in range(len(shifts)):
            new_list[shifts[idx]] = txt[idx]
            
        return cls.convert_to_str(new_list)
        

    @classmethod
    def convert_to_str(cls,chars_list):
        return ''.join(chars_list)

    @classmethod
    def shuffle_bin(cls,txt,key):
        temp = txt 
        keys = Keys.create_list(key,(64)*2)

        for idx in range(len(keys)):
            temp = cls.shuffle_helper(temp,keys[idx])

        return temp

    @classmethod
    def un_shuffle_bin(cls,txt,key):
        temp = txt 
        keys = Keys.create_list(key,(64)*2)

        for idx in range(len(keys)):
            temp = cls.un_shuffle_helper(temp,keys[len(keys)-1-idx])
        return temp

    @classmethod
    def shuffle_helper(cls,txt,key):
        dict1,dict2 = Dict_Tools.get_dicts(key)
        new_txt = []

        for char in txt:
            temp = bin(dict2[char])[2:]  
            temp = ''.join(['0' for _ in range(len(temp),BITS_SIZE)]) + temp
            new_txt.append(temp)    

        shuffled_bytes =  Block_Tools.split_to_parts(cls.shuffle(''.join(new_txt),key),BITS_SIZE)

        return ''.join(dict1[int(block.bytes,2)] for block in shuffled_bytes)

    @classmethod
    def un_shuffle_helper(cls,txt,key):
        dict1,dict2 = Dict_Tools.get_dicts(key)
        new_txt = []

        for char in txt:
            temp = bin(dict2[char])[2:]  
            temp = ''.join(['0' for _ in range(len(temp), BITS_SIZE)]) + temp
            new_txt.append(temp)  

        shuffled_bytes =  Block_Tools.split_to_parts(cls.un_shuffle(''.join(new_txt),key), BITS_SIZE)
        return ''.join(dict1[int(block.bytes,2)] for block in shuffled_bytes)