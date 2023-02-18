from .characters_list import get_characters_list

from numpy import array,empty,  ndarray
from hashlib import sha256,shake_256,md5,blake2s,sha3_256,sha3_512

from typing import List ,Callable
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
    def str_to_blake2s(cls,txt: str) -> str:
        return blake2s(txt.encode()).hexdigest()

    @classmethod
    def convert_to_hash(cls,txt: str) -> str:
        txt = cls.str_to_shake_256(txt)
        txt = cls.str_to_md5_sha3_512(txt)
        txt = cls.str_to_blake2s(txt)
        txt = cls.str_to_sha3_256(txt)
        txt = cls.str_to_sha256(txt)
        return txt

    @classmethod
    def get_hash_funcs(cls) -> List[str]:
        return ['str_to_shake_256','str_to_md5_sha3_512' , 'str_to_blake2s','str_to_sha3_256','str_to_sha256']

    @classmethod
    def random_convert_to_hash(cls,hash_funcs: List[str]) -> callable[[str], str]:

        def convert_to_hash(txt: str) -> str: 
            for hash_func_name in hash_funcs:
                if not hasattr(cls,hash_func_name):
                    raise KeyError(f"Hash function name must either implmented into Keys classs or  be one of the following {cls.get_hash_funcs()}")

                hash_func = getattr(cls,hash_func_name)
                txt = hash_func(txt)
            return txt 

        cls.custom_convert_to_hash = convert_to_hash
        return convert_to_hash

    @classmethod
    def custom_convert_to_hash(cls,txt: str) -> Callable[[str], str]:
        return cls.convert_to_hash(txt)

    @classmethod 
    def create_list(cls, Key: str, size:int, add_to_half: int  = 1) -> ndarray:
        keys = array([Key])

        for _ in range(get_nearist_2_power_until_64(size)):
            keys = cls.create_list_helper(keys,add_to_half)
            
        return keys

    # this method take one parameter (hash as a string) and then returns the hashs of the two halfs of the key
    @classmethod
    def split_and_hash(cls, key:str ,add_to_half:int = 1) -> List[str, str]:
        half_key = (len(key) // 2) + add_to_half
        return [cls.custom_convert_to_hash(key[half_key:]), cls.custom_convert_to_hash(key[:half_key])]

    # takes a list of hashes and return a twice as big list from spliting anf hashing each hash
    @classmethod
    def create_list_helper(cls, keys:str , add_to_half:int = 1) -> ndarray:
        new_keys = empty(len(keys) * 2, dtype='<U65')

        for idx, key in enumerate(keys):
            left,right = cls.split_and_hash(key, add_to_half)
            new_keys[idx] = left
            new_keys[-(idx + 1)] = right

        return new_keys

    # write the  generated list from create_list_helper in a file called keys.txt
    @classmethod
    def create_hash_list(cls, key:str, size: int, add_to_half:int = 1) -> ndarray:
        keys_list = cls.create_list(key, size * 5,add_to_half)
        result = "".join(keys_list)
        return array([ord(_char) for _char in result]), keys_list

    """ takes the size of the text that to be encrypted  and takes the key to genrate keylist using the class
     method create_hash_list and then take  the  series of hashes and pass it to the nums classmethod"""
    @classmethod
    def generate_keylist(cls, txt_size: int, key: str, add_to_half:int = 1,case: str = "NONE") -> List[int]:
        hash_keys,_ = cls.create_hash_list(key, txt_size,add_to_half)
        num_list = []

        for idx in range(1, (len(hash_keys) // 5) + 1):
            temp_list = hash_keys[(idx * 5) - 5  :idx * 5]
            num_list.append(cls.generate_nums(temp_list,case)) 

        return num_list

    """ takes  a list of len 5 and genrate a number from it to pass it back to  generate_keylist """
    @classmethod
    def generate_nums(cls, numbers_list: List[int], Case: str ='NONE') -> int : 

        len_chars = len(get_characters_list())
        num1 = 0
        numbers_list = [ int(num) for num in numbers_list]

        if len(numbers_list) < 4:
            raise ValueError("Templist should  consist of at least 5 items")

        try:
            num1 += int((((numbers_list[2] ** numbers_list[1]) ^
                        numbers_list[0]) * numbers_list[4]) // numbers_list[3]) % len_chars
            # in cases where numbers_list[3] can be zero so thats why we used try/execpt here
            if Case != 'NONE':
                if num1 == 0:
                    num1 = int(
                        (((numbers_list[1] ** numbers_list[3]) + numbers_list[2]) ^ numbers_list[4]) // numbers_list[0]) % len_chars

                if num1 == 0:
                    num1 = int((  (numbers_list[0] + numbers_list[1] +
                            numbers_list[2] ) ** (numbers_list[3] ^ numbers_list[4])) // 3) % len_chars


        except ZeroDivisionError:
            # provides two alternative number if num1 has an error
            try:
                num1 = int(
                    (((numbers_list[1] ** numbers_list[3]) ^ numbers_list[2]) * numbers_list[4]) // numbers_list[0]) % len_chars

            except ZeroDivisionError:
                """num1 cann't have an error because it uses only addtion it can only be 0 if all the i
                tems in numbers_list is zero which is rare to happen """

                num1 = int((  (numbers_list[0] ^ numbers_list[1] ^
                        numbers_list[2] ) ** (numbers_list[3] * numbers_list[4])) // 3) % len_chars

        return num1

def get_nearist_2_power_until_64(num: int) -> int:
    counter = 0
    while num > 64 :
        num //= 2
        counter += 1
    return counter 