from enc import Enc , Block_Enc

class AE:
    # encrypts the text that was given
    def __init__(self,key):
        self.stream_number = 1
        self.cur_keys_list = []
        self.key = Enc.convert_to_hash(key)

    @classmethod
    def Encrypt(cls, text, key):
        hashed_key = Enc.convert_to_hash(key)
        len_text = len(text)
        num_list = Enc.generate_keylist(len_text * 1.5, hashed_key)
        encoded = ''
        dict1, dict2 = Enc.get_dicts(hashed_key)

        for idx in range(len_text):
            temp_num = dict2[text[idx]] + num_list[idx]
            temp_char = dict1[(temp_num % len(dict1.keys()))]
            encoded += temp_char

        return encoded

    @classmethod
    def Decrypt(cls, endcoded, key):
        len_text = len(endcoded)
        hashed_key = Enc.convert_to_hash(key)
        num_list = Enc.generate_keylist(len_text * 1.5, hashed_key)
        decoded = ''
        dict1, dict2 = Enc.get_dicts(hashed_key)

        for idx in range(len_text):
            temp_num = (dict2[endcoded[idx]] - num_list[idx]) % len(dict1.keys())
            temp_char = dict1[temp_num ]
            decoded += temp_char
        
        return decoded

    @classmethod
    def Encrypt_with_shuffling(cls, txt, key):
        hashed_key = Enc.convert_to_hash(key)
        txt = Enc.shuffle(txt, hashed_key)
        return cls.Encrypt(txt, key)

    @classmethod
    def Decrypt_with_shuffling(cls, encoded, key):
        hashed_key = Enc.convert_to_hash(key)
        encoded = cls.Decrypt(encoded, key)
        return Enc.un_shuffle(encoded, hashed_key)


    def Stream(self,text):
        len_text = len(text)
        if len(self.cur_keys_list) < len_text:
            self.cur_keys_list.extend(Enc.generate_keylist(len_text * 1.5 * self.stream_number, self.key))
            self.stream_number += 1
            
        encoded = ''
        dict1, dict2 = Enc.get_dicts(self.key)

        for idx in range(len_text):
            temp_num = dict2[text[idx]] + self.cur_keys_list.pop(0)
            temp_char = dict1[(temp_num % len(dict1.keys()))]
            encoded += temp_char

        return encoded

    def Decrypt_Stream(self,encoded):
        len_text = len(encoded)
        if len(self.cur_keys_list) < len_text:
            self.cur_keys_list.extend(Enc.generate_keylist(len_text * 1.5 * self.stream_number, self.key))
            self.stream_number += 1
        decoded = ''
        dict1, dict2 = Enc.get_dicts(self.key)

        for idx in range(len_text):
            temp_num = (dict2[encoded[idx]]-self.cur_keys_list.pop(0)) % len(dict1.keys())
            temp_char = dict1[temp_num]
            decoded += temp_char

        return decoded

    @classmethod
    def Block_Encryption(cls,text, key):
        if len(text) % 64 != 0:
            for i in range(64 - (len(text) % 64)):
                text+= "%"
        size = len(text) +((len(text) % 64) - 64 )
        hashed_key = Enc.convert_to_hash(key)

        text = cls.Encrypt(text,key)
        un_joind = Enc.create_hash_list(hashed_key, size)
        key_list = ["".join(un_joind[idx * 64 : (idx +1) * 64]) for idx in range(len(un_joind) // 64)]

        blocks = Block_Enc.split_to_parts(text,64)
        Block_Enc.mix_blocks(blocks,key_list)
        dict_1, dict_2 = Enc.get_dicts(hashed_key)

        for idx in range(len(blocks)):
            blocks[idx].bytes = Block_Enc.xor_str(blocks[idx].bytes, key_list[idx],dict_1, dict_2)

        
        result = list(Block_Enc.connect_blocks(blocks))

        while result[-1] == "%":
            result.pop()

        return "".join(result)
            
    @classmethod
    def Block_Decryption(cls,text, key):
        size = len(text) +((len(text) % 64) - 64 )
        hashed_key = Enc.convert_to_hash(key)

        un_joind = Enc.create_hash_list(hashed_key, size)
        key_list = ["".join(un_joind[idx * 64 : (idx +1) * 64]) for idx in range(len(un_joind) // 64)]

        blocks = Block_Enc.split_to_parts(text,64)
        dict_1, dict_2 = Enc.get_dicts(hashed_key)

        for idx in range(len(blocks)):
            blocks[idx].bytes = Block_Enc.xor_str(blocks[idx].bytes, key_list[idx],dict_1, dict_2, False)

        Block_Enc.un_mix_blocks(blocks, key_list)
        result = list(Block_Enc.connect_blocks(blocks))
        result = list(cls.Decrypt(result,key))

        while result[-1] == "%":
            result.pop()
        
        return "".join(result)
