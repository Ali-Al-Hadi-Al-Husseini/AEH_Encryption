
from enc import Enc
from os import remove
from hashlib import sha256

class AEH:
    # encrypts the text that was given

    @classmethod
    def Encrypt(cls,text, key):
        hashed_key = sha256(key.encode()).hexdigest()
        len_text = len(text)
        num_list = Enc.generate_keylist(len_text * 1.5, hashed_key)
        encoded = ''
        dict1, dict2 = Enc.get_dicts(key)
        for idx in range(len_text):
            temp_num = dict2[text[idx]] + num_list[idx]
            temp_char = dict1[( temp_num % len(dict1))]
            encoded += temp_char

        remove('keys.txt')
        return encoded

    @classmethod
    def Decrypt(cls,endcoded,key):
        len_text = len(endcoded)
        hashed_key = sha256(key.encode()).hexdigest()
        num_list = Enc.generate_keylist(len_text, hashed_key)
        decoded = ''
        dict1, dict2 = Enc.get_dicts(key)

        for idx in range(len_text):
            temp_num = (dict2[endcoded[idx]]-num_list[idx]) % len(dict1)
            temp_char = dict1[temp_num]
            decoded += temp_char
        remove('keys.txt')
        return decoded
    
