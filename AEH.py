
from enc import Enc
from os import remove
from hashlib import sha256


class AEH:
    # encrypts the text that was given

    @classmethod
    def Encrypt(cls,text, key):
        hashed_key = Enc.convert_to_hash(key)
        len_text = len(text)
        num_list = Enc.generate_keylist(len_text * 1.5, hashed_key)
        encoded = ''
        dict1, dict2 = Enc.get_dicts(hashed_key)

        for idx in range(len_text):
            temp_num = dict2[text[idx]] + num_list[idx]
            temp_char = dict1[( temp_num % len(dict1.keys()))]
            encoded += temp_char

        remove('keys.txt')
        return encoded

    @classmethod
    def Decrypt(cls,endcoded,key):
        len_text = len(endcoded)
        hashed_key = Enc.convert_to_hash(key)
        num_list = Enc.generate_keylist(len_text * 1.5, hashed_key)
        decoded = ''
        dict1, dict2 = Enc.get_dicts(hashed_key)
        
        for idx in range(len_text):
            temp_num = (dict2[endcoded[idx]]-num_list[idx]) % len(dict1.keys())
            temp_char = dict1[temp_num]
            decoded += temp_char
        remove('keys.txt')
        return decoded
    
    @classmethod
    def Encrypt_with_shuffling(cls,txt,key):
        hashed_key = Enc.convert_to_hash(key)
        txt = Enc.shuffle(txt,hashed_key)
        return cls.Encrypt(txt,key)

    @classmethod
    def Decrypt_with_shuffling(cls,encoded, key):
        hashed_key = Enc.convert_to_hash(key)   
        encoded = cls.Decrypt(encoded,key)
        return Enc.un_shuffle(encoded, hashed_key)




