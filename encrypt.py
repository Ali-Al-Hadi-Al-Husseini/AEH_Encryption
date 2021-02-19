import os
from hashlib import sha256
from enc import Enc
#687

class AEH:
    # encrypts the text that was given
    @classmethod
    def Encrypt(cls,text, key, name = 'Encrypted_By_AEH'):
        len_text = len(text)
        num_list = cls.generate_keylist(len_text, key)
        encoded = ''
        for char in range(len_text):
            #Not done yet
            pass



        
    #generates a key by using Enc from enc.py
    @classmethod
    def generate_keylist(cls,txt_size,key):
        Enc.create_file(key, txt_size)
        num_list = []

        with open('keys.txt','r') as keys:
            key = keys.read()

            for idx in range(1, int(len(key) // 5) + 1):
                if idx > len(key):
                    break

                else:
                    temp_list = key[(idx * 5) - 5:idx * 5]
                    num = ((( temp_list[2] ** temp_list[1]) + temp_list[0]) *temp_list[4] ) // temp_list[3]
                    num_list.append(num)
        os.remove('key.text')
        return num_list