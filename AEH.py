
from enc import Enc
from os import remove
from hashlib import sha256


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

        remove('keys.txt')
        return encoded

    @classmethod
    def Decrypt(cls, endcoded, key):
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
    def Encrypt_with_shuffling(cls, txt, key):
        hashed_key = Enc.convert_to_hash(key)
        txt = Enc.shuffle(txt, hashed_key)
        return cls.Encrypt(txt, key)

    @classmethod
    def Decrypt_with_shuffling(cls, encoded, key):
        hashed_key = Enc.convert_to_hash(key)
        encoded = cls.Decrypt(encoded, key)
        return Enc.un_shuffle(encoded, hashed_key)


    def stream(self,text):
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

        remove('keys.txt')
        return encoded

    def decrypt_stream(self,encoded):
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

        remove('keys.txt')
        return decoded
