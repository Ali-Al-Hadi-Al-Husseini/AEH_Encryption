from .Encryption_Tools.String_tools import String_tools
from .Encryption_Tools.Dict_tools import Dict_Tools
from .Encryption_Tools.keys_tools import Keys


from .block.Block_tools import Block_Tools,Shuffle
from .Encryption_Tools.characters_list import get_characters_list
from random import randrange


class AE:
    # encrypts the text that was given
    def __init__(self,key):
        self.stream_number = 1
        self.cur_keys_list = []
        self.un_hashed = key
        self.key = Keys.convert_to_hash(key)

    @classmethod
    def Encrypt(cls, text, key,add_to_half= 1,character_list = None):
        hashed_key = Keys.convert_to_hash(key)
        len_text = len(text)
        num_list = Keys.generate_keylist(len_text * 3 * (len_text % 10+1), hashed_key,add_to_half)
        encoded = ''
        dict1, dict2 = Dict_Tools.get_dicts(hashed_key,character_list)

        for idx in range(len_text):
            temp_num = dict2[text[idx]] + num_list[idx]
            temp_char = dict1[(temp_num % len(dict1.keys()))]
            encoded += temp_char

        return encoded

    @classmethod
    def Decrypt(cls, endcoded, key,add_to_half= 1,character_list = None):
        len_text = len(endcoded)
        hashed_key = Keys.convert_to_hash(key)
        num_list = Keys.generate_keylist(len_text * 3 * (len_text%10 + 1) , hashed_key,add_to_half)
        decoded = ''
        dict1, dict2 = Dict_Tools.get_dicts(hashed_key,character_list)

        for idx in range(len_text):
            temp_num = (dict2[endcoded[idx]] - num_list[idx]) % len(dict1.keys())
            temp_char = dict1[temp_num ]
            decoded += temp_char
        
        return decoded

    @classmethod
    def Encrypt_with_shuffling(cls, txt, key):
        hashed_key = Keys.convert_to_hash(key)
        txt =  Shuffle.shuffle(txt, hashed_key)
        return cls.Encrypt(txt, key)

    @classmethod
    def Decrypt_with_shuffling(cls, encoded, key):
        hashed_key = Keys.convert_to_hash(key)
        encoded = cls.Decrypt(encoded, key)
        return  Shuffle.un_shuffle(encoded, hashed_key)


    def Stream(self,text):
        len_text = len(text)
        if len(self.cur_keys_list) < len_text:
            self.cur_keys_list.extend(Keys.generate_keylist(len_text * 1.5 * self.stream_number, self.key))
            self.stream_number += 1
            
        encoded = ''
        dict1, dict2 = Dict_Tools.get_dicts(self.key)

        for idx in range(len_text):
            temp_num = dict2[text[idx]] + self.cur_keys_list.pop(0)
            temp_char = dict1[(temp_num % len(dict1.keys()))]
            encoded += temp_char

        return encoded

    def Decrypt_Stream(self,encoded):
        len_text = len(encoded)
        if len(self.cur_keys_list) < len_text:
            self.cur_keys_list.extend(Keys.generate_keylist(len_text * 1.5 * self.stream_number, self.key))
            self.stream_number += 1
        decoded = ''
        dict1, dict2 = Dict_Tools.get_dicts(self.key)

        for idx in range(len_text):
            temp_num = (dict2[encoded[idx]]-self.cur_keys_list.pop(0)) % len(dict1.keys())
            temp_char = dict1[temp_num]
            decoded += temp_char

        return decoded

    @classmethod
    def Block_Encryption(cls,text, key):

        if len(text) % 64 != 0:
            for _ in range(64 - (len(text) % 64)):
                text+= "%"



        size = len(text) +((64 - (len(text) % 64)  ))
        hashed_key = Keys.convert_to_hash(key)
        dict_1, dict_2 = Dict_Tools.get_dicts(hashed_key)
        shift = 0 

        for char in hashed_key:
            shift += dict_2[char] 
        
        shift *= 13
        shift %= size

        text =  String_tools.string_bit_shift(text,dict_1,dict_2,shift)
        text = cls.Encrypt(text,key)
        _,key_list = Keys.create_hash_list(hashed_key, size)


        blocks = Block_Tools.split_to_parts(text,64)
        #to speed up uncomment and use mix_blocks_process
        # but you need to run under if __name__ == '__main__':

        blocks = Block_Tools.mix_blocks(blocks,key_list)

        Block_Tools.xor_blocks(blocks,key_list,dict_1,dict_2)    

        
        result = list(Block_Tools.connect_blocks(blocks))


        if len(result) > 0 :
            while result[-1] == "%":
                result.pop()

        result = "".join(result)

        return result
            
    @classmethod
    def Block_Decryption(cls,text, key,last=True):
        size = len(text) +((64 - (len(text) % 64)))
        hashed_key = Keys.convert_to_hash(key)

        _,key_list  =Keys.create_hash_list(hashed_key, size)

        
        blocks = Block_Tools.split_to_parts(text,64)
        dict_1, dict_2 = Dict_Tools.get_dicts(hashed_key)

        Block_Tools.xor_blocks(blocks,key_list,dict_1,dict_2)
        #to speed up uncomment and use unmix_blocks_process in enc.py file
        # but you need to run under if __name__ == '__main__':
        
        blocks = Block_Tools.un_mix_blocks(blocks, key_list)
        result = list(Block_Tools.connect_blocks(blocks))
        result = list(cls.Decrypt(result,key))

        shift = 0
        for char in hashed_key:
            shift += dict_2[char]

        shift *= 13
        shift %= size

        result = list(String_tools.string_bit_shift(''.join(result),dict_1,dict_2,shift,False))
        
        if last and len(result) > 0:
            while result[-1] == "%":
                result.pop()
            
        return "".join(result)

    @classmethod
    def block_encryption_rounds(cls,text,key,rounds=6):
        key_list = Keys.create_list(Keys.convert_to_hash(key),(rounds) *64)
        temp = text

        for idx in range(len(key_list)):
            temp = cls.Block_Encryption(temp,key_list[idx])
        
        return temp

    @classmethod
    def block_decryption_rounds(cls,text,key,rounds=6):
        key_list = Keys.create_list(Keys.convert_to_hash(key),(rounds) * 64)
        temp = text

        for idx in range(len(key_list)):
            Hash = key_list[len(key_list)-1-idx]
            temp = cls.Block_Decryption(temp,Hash,idx == (len(key_list) - 1))
        
        return temp

    
    @classmethod
    def professional_encryption(cls,text: str,key: str,add_to_hash_half: int):
        if len(key) < 64 : 
            raise ValueError("Key is to Short")

        if 0  > add_to_hash_half  or  add_to_hash_half > (len(key) // 4): 
            raise ValueError("add to hash half number should be between 1 and the length of the key divided by 4")

        if len(text) % 64 != 0:
            for i in range(64 - (len(text) % 64)):
                text+= "%"

        size = len(text) +((len(text) % 64) - 64 )
        hashed_key = Keys.convert_to_hash(key)

        
        _,key_list = Keys.create_hash_list(hashed_key, size, add_to_hash_half)
        character_list =  Shuffle.shuffle(get_characters_list(),key_list[randrange(0,len(key_list))])

        random_convert_to_hash_list = Shuffle.list_shuffle(Keys.get_hash_funcs(),key_list[randrange(0,len(key_list))])
        convert_to_hash = Keys.random_convert_to_hash(random_convert_to_hash_list)

        new_key = hashed_key + character_list
        hashed_key = convert_to_hash(new_key)

        _,key_list = Keys.create_hash_list(hashed_key, size, add_to_hash_half)

        text = cls.Encrypt(text, key, add_to_hash_half, character_list)

        blocks = Block_Tools.split_to_parts(text,64)
        #to speed up up uncomment and use mix_blocks_process
        # but you need to run under if __name__ == '__main__':
        blocks =Block_Tools.mix_blocks(blocks,key_list)
        dict_1, dict_2 = Dict_Tools.get_dicts(hashed_key,character_list)

        # to speed up uncomment and use xor_blocks_process
        # but you need to run under if __name__ == '__main__':
        Block_Tools.xor_blocks(blocks,key_list,dict_1,dict_2)

        
        result = list(Block_Tools.connect_blocks(blocks))

        return "".join(result), character_list,random_convert_to_hash_list

    @classmethod
    def professional_decryption(cls,text: str,key: str,add_to_hash_half: int,character_list: list, random_convert_to_hash_list):
        if 0  > add_to_hash_half  or  add_to_hash_half > (len(key) // 4): 
            raise ValueError("add to hash half number should be between 1 and the length on the key divided by 4")

        size = len(text) +((len(text) % 64) - 64 )
        hashed_key = Keys.convert_to_hash(key)
        new_key = hashed_key + character_list

        convert_to_hash = Keys.random_convert_to_hash(random_convert_to_hash_list)
        hashed_key = convert_to_hash(new_key)

        _,key_list  =Keys.create_hash_list(hashed_key, size, add_to_hash_half)

        
        blocks = Block_Tools.split_to_parts(text,64)
        dict_1, dict_2 = Dict_Tools.get_dicts(hashed_key,character_list)

        Block_Tools.xor_blocks(blocks,key_list,dict_1,dict_2)
        #to speed up use un_mix_blocks_process
        # but you need to run under if __name__ == '__main__':
        blocks = Block_Tools.un_mix_blocks(blocks, key_list)
        result = list(Block_Tools.connect_blocks(blocks))
        result = list(cls.Decrypt(result,key,add_to_hash_half,character_list))

        if len(result) > 0 :
            while result[-1] == "%":
                result.pop()
            
        return "".join(result)

    @classmethod
    def professional_block_encryption_rounds(cls,text: str,key: str,add_to_hash_half: int,rounds=6):
        if len(key) < 64 : 
            raise ValueError("Key is to Short")

        if 0  > add_to_hash_half  or  add_to_hash_half > (len(key) // 4): 
            raise ValueError("add to hash half number should be between 1 and the length of the key divided by 4")

        key_list = Keys.create_list(Keys.convert_to_hash(key),(rounds) * 64)
        temp = text
        chars_list = []
        hash_funcs = []

        for idx in range(len(key_list)):
            temp,chars, hash_func = cls.professional_encryption(temp,key_list[idx],add_to_hash_half)
            chars_list.append(chars)
            hash_funcs.append(hash_func)

        return temp ,chars_list,hash_funcs

    @classmethod
    def professional_block_decryption_rounds(cls,text: str,key: str,add_to_hash_half: int,characters_list: list,hash_funcs,rounds=6):
        if 0  > add_to_hash_half  or  add_to_hash_half > (len(key) // 4): 
            raise ValueError("add to hash half number should be between 1 and the length of the key divided by 4")

        key_list = Keys.create_list(Keys.convert_to_hash(key),(rounds) * 64)
        temp = text

        for idx in range(len(key_list)):
            temp = cls.professional_decryption(temp,key_list[len(key_list)-1-idx],add_to_hash_half,characters_list[len(characters_list)-1-idx],hash_funcs[len(characters_list)-1-idx])
        
        return temp


# if __name__ == "__main__":
#     print('started')
#     a,_ = AE.professional_encryption('holame amigoad asd asdaskdhsajkdhsahdajskdhjasd' * 100000,"hola me amaghio" * 8,6)
#     print('started')
#     print(a)
#     s = open('temp.txt','a',encoding="utf-8")
#     s.write(a)
#     s.close()
