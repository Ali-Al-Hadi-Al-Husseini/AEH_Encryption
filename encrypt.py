
from hashlib import sha256
from enc import Enc

class AEH:
    # encrypts the text that was given

    @classmethod
    def Encrypt(cls,text, key):
        len_text = len(text)
        num_list = Enc.generate_keylist(len_text, key)
        encoded = ''
        dict1, dict2 = Enc.get_dicts()

        for idx in range(len_text):
            temp_num = dict2[text[idx]] + num_list[idx]
            temp_char = dict1[( temp_num % 84)]
            encoded += temp_char

        return encoded

    @classmethod
    def Decrypt(cls,endcoded,key):
        len_text = len(endcoded)
        num_list = Enc.generate_keylist(len_text, key)
        decoded = ''
        dict1, dict2 = Enc.get_dicts()

        for idx in range(len_text):
            temp_num = (dict2[endcoded[idx]]-num_list[idx]) % 84
            temp_char = dict1[temp_num]
            decoded += temp_char

        return decoded
    

x = 'mousdylilo98'
y = 'lit'
z = AEH.Encrypt(x,y)
print(z)
print(AEH.Decrypt(z,y))
