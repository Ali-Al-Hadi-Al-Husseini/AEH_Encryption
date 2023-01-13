from .characters_list import get_characters_list

from numpy import array,empty
from hashlib import sha256,shake_256,md5,blake2s,sha3_256,sha3_512
import hashlib

class Keys:

    @classmethod
    def str_to_sha256(cls,txt:str) -> str:
        return sha256(txt.encode()).hexdigest()
    @classmethod
    def str_to_sha3_256(cls,txt:str) -> str:
        return sha3_256(txt.encode()).hexdigest()

    @classmethod
    def str_to_md5_sha3_512(cls,txt:str) -> str:
        txt = sha3_512(txt.encode()).hexdigest()

        return md5(txt[:len(txt)].encode()).hexdigest() + md5(txt[len(txt):].encode()).hexdigest()

    @classmethod
    def str_to_shake_256(cls,txt:str) -> str:
        return shake_256(txt.encode()).hexdigest(32)

    @classmethod
    def str_to_blake2s(cls,txt:str) -> str:
        return blake2s(txt.encode()).hexdigest()

    @classmethod
    def convert_to_hash(cls,txt):
        txt = (cls.str_to_shake_256(txt))
        txt = (cls.str_to_sha256(txt))
        txt = (cls.str_to_md5_sha3_512(txt))
        txt = (cls.str_to_blake2s(txt))
        txt = (cls.str_to_sha3_256(txt))
        return txt

    @classmethod
    def create_list(cls, Key, size,add_to_half = 1):
        keys = array([Key])
        for _ in range(get_nearist_2_power_until_64(size)):
            keys = cls.create_list_helper(keys,add_to_half)
            
        return keys

    # this method take one parameter (hash as a string) and then returns the hashs of the two halfs of the key
    @classmethod
    def split_and_hash(cls, key,add_to_half = 1):
        half_key = (len(key) // 2) + add_to_half
        return [cls.convert_to_hash(key[half_key:]),cls.convert_to_hash(key[:half_key])]

    # takes a list of hashes and return a twice as big list from spliting anf hashing each hash
    @classmethod
    def create_list_helper(cls, keys, add_to_half=1 ):
        new_keys = empty((len(keys) * 2),dtype='<U65')
        idx = 0 
        for key in keys:
            left,right = cls.split_and_hash(key, add_to_half)
            new_keys[idx] = left
            idx+=1 
            new_keys[idx] = right
            idx += 1 
        return new_keys

    # write the  generated list from create_list_helper in a file called keys.txt
    @classmethod
    def create_hash_list(cls, key, size,add_to_half = 1):
        keys_list = cls.create_list(key, size * 5,add_to_half)
        result = "".join(keys_list)
        return array([ord(_char) for _char in result]),keys_list

    """ takes the size of the text that to be encrypted  and takes the key to genrate the file (keys.txt) using the class
     method create_hash_list adn then take  the  series of hashes and pass it to the nums classmethod"""
    @classmethod
    def generate_keylist(cls, txt_size, key, add_to_half = 1,case="NONE"):
        key,_ = cls.create_hash_list(key, txt_size,add_to_half)
        num_list = []

        for idx in range(1, (len(key) // 5) + 1):
            temp_list = key[(idx * 5) - 5  :idx * 5]
            num_list.append(cls.generate_nums(temp_list,case)) 

        return num_list

    """ takes  a list of len 5 and genrate a number from it to pass it back to  generate_keylist """
    @classmethod
    def generate_nums(cls, temp_list,Case='NONE'):

        len_chars = len(get_characters_list())
        num1 = 0
        temp_list = [ int(num) for num in temp_list]

        if len(temp_list) >= 4:
            try:
                num1 += int((((temp_list[2] ** temp_list[1]) +
                            temp_list[0]) * temp_list[4]) // temp_list[3]) % len_chars
                # in cases where temp_list[3] can be zero so thats why we used try/execpt here
                if Case != 'NONE':
                    if num1 == 0:
                        num1 = int(
                            (((temp_list[1] ** temp_list[3]) + temp_list[2]) * temp_list[4]) // temp_list[0]) % len_chars

                    if num1 == 0:
                        num1 = int((  (temp_list[0] + temp_list[1] +
                                temp_list[2] ) ** (temp_list[3] * temp_list[4])) // 3) % len_chars


            except ZeroDivisionError:
                # provides two alternative number if num1 has an error
                try:
                    num1 = int(
                        (((temp_list[1] ** temp_list[3]) + temp_list[2]) * temp_list[4]) // temp_list[0]) % len_chars

                except ZeroDivisionError:
                    """num1 cann't have an error because it uses only addtion it can only be 0 if all the i
                    tems in temp_list is zero which is rare to happen """

                    num1 = int((  (temp_list[0] + temp_list[1] +
                            temp_list[2] ) ** (temp_list[3] * temp_list[4])) // 3) % len_chars

            return num1

        else:
            raise ValueError("Templist should be consist of at least 5 items")
    

    

def get_nearist_2_power_until_64(num):
    counter = 0
    while num > 64 :
        num //= 2
        counter += 1
    return counter 