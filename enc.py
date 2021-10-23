from hashlib import new, sha256


class Enc:

    # creater a string that is as the size of the file from hashes using sha256
    @classmethod
    def create_list(cls, Key, size):
        if size <= 64:
            new_key = [Key]
            return new_key

        else:
            new_keys = []
            new_list = cls.create_new_list(cls.create_list(Key, (size // 2)))
            new_keys.extend(new_list)
            return new_keys

    # this method take one parameter (hash as a string) and then returns the hashs of the two halfs of the key
    @classmethod
    def split_and_hash(cls, key):
        half_key = int(len(key) / 2) + 1
        return list((sha256(key[half_key:].encode()).hexdigest(), sha256(key[:half_key].encode()).hexdigest()))

    # takes a list of hashes and return a twice as big list from spliting anf hashing each hash
    @classmethod
    def create_new_list(cls, keys):
        new_keys = []
        for key in keys:
            new_keys.extend(cls.split_and_hash(key))

        return new_keys

    # write the  generated list from create_new_list in a file called keys.txt
    @classmethod
    def create_hash_list(cls, key, size):
        keys_list = cls.create_list(key, size * 5)
        result = ""
        for key in keys_list:
            result += key
        return list(result)

    """ takes the size of the text that to be encrypted  and takes the key to genrate the file (keys.txt) using the class
     method create_hash_list adn then take  the  series of hashes and pass it to the nums classmethod"""
    @classmethod
    def generate_keylist(cls, txt_size, key,case="NONE"):
        key = cls.create_hash_list(key, txt_size)
        num_list = []

        for idx in range(1, int(len(key) // 5) + 1):
            if idx > len(key):
                break

            else:
                temp_list = key[(idx * 5) - 5  :idx * 5]
                num_list.append(cls.generate_nums(temp_list,case)) 

        return num_list

    """ takes  a list of len 5 and genrate a number from it to pass it back to  generate_keylist """
    @classmethod
    def generate_nums(cls, temp_list,Case='NONE'):
        # checks to see if ther are any letter in the list and then change it to numbers
        for idx in range(len(temp_list)):
            if type(temp_list[idx]) == str:
                temp_list[idx] = ord(temp_list[idx])

        # this block genrates new number from the five number in the temp_list
        len_chars = len(cls.get_character_list())
        num1 = 0

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
                """num3 cann't have an error because it uses only addtion it can only be 0 if all the i
                tems in temp_list is zero which is to rare to happen """

                num1 = int((  (temp_list[0] + temp_list[1] +
                          temp_list[2] ) ** (temp_list[3] * temp_list[4])) // 3) % len_chars

        return num1


    # converts  a list which is normally passed from the class method generate_new_dicts
    @classmethod
    def convert_to_dict(cls, character_list):
        dict1 = {}

        for i in range(len(character_list)):
            dict1[i] = character_list[i]

        return dict1

    # returns a new dict where the keys are the value and vice versa
    @classmethod
    def reverse_dict(cls, dict1):
        new_dict = {}

        for key, value in dict1.items():
            new_dict[value] = key
        return new_dict

    """take a key and generates a new list with different order  of the letters (changes the index of each letter and give a new_list)
    which means every key have different order of letter which makes it a bit harder to crack it """
    @classmethod
    def generate_character_list(cls, key):
        character_list = cls.get_character_list()

        new_character_list = []
        keys = cls.generate_keylist(len(character_list), key,'A')

        for idx in range(len(character_list)):
            new_character_list.append(character_list.pop(
                keys[idx] % len(character_list)))

        return new_character_list

    @classmethod
    def get_dicts(cls, key):
        character_list = cls.generate_character_list(key)
        dict1 = cls.convert_to_dict(character_list)
        dict2 = cls.reverse_dict(dict1)

        return dict1, dict2

    @classmethod
    def get_character_list(cls):
        return ["'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4',
                '5', '6','7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E',
                'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g',
                'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', ' ', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                'y', 'z', 'p', '\n', '…', '!', '’', '→', '‘', '“', '”', '{', '}', '"', '&', '—', '×',
                '–', '%', '#', 'ض', 'ص', 'ث', 'ق',
                'ف', 'غ', 'ع', 'ه', 'خ', 'ح', 'ج', 'د', 'ط', 'ك', 'م', 'ن', 'ت', 'ا', 'ل'
                ,'ب', 'ي', 'س', 'ش', 'ئ', 'ء', 'ؤ', 'ر', 'ﻻ', 'ى', 'ة', 'و', 'ز', 'ظ','|',"ˈ","ɪ",'ɛ','ʁ',
                'ʔ', 'ʃ', 'ü', 'ö', 'ć', '\t', 'ô', 'é', 'ä', 'ó', 'Ă', '$', 'İ', 'á', 'ï', 'î', 'Ü'
                ,'ø', 'ß', 'æ', 'Ö', 'í', 'à', 'Б', 'е', 'л', 'а', 'р', 'у', 'с', 'к', 'я', 'ی', 'ç', 'Հ', 'ա',
                'յ', 'ե', 'ր', 'ն', '®','Χ', 'Ψ', 'Ω', 'Ϊ', 'Ϋ', 'ά', 'έ', 'ή', 'ί', 'ΰ', 'α', 'β', 'γ',
                'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'ς',
                'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω', 'ϊ', 'ϋ', 'ό', 'ύ', 'ώ', 'Ϗ', 'ϐ', 'ϑ',
                'ϒ', 'ϓ', 'ϔ', 'ϕ', 'ϖ', 'ϗ', 'Ϙ', 'ϙ', 'Ϛ', 'ϛ', 'Ϝ', 'ϝ', 'Ϟ', 'ϟ', 'Ϡ','Ĥ'
                , 'ϡ', 'Ϣ', 'ϣ', 'Ϥ', 'ϥ', 'Ϧ', 'ϧ','Ɗ', 'Ƌ', 'ƌ', 'ƍ', 'Ǝ', 'Ə', 'Ɛ', 'Ɠ', '~']
    
    @classmethod
    def convert_to_hash(cls,txt):
        return sha256(txt.encode()).hexdigest()

    @classmethod
    def generate_shuffle_list(cls,len_txt,key):
        new_nums = []
        nums = []
        temp_num = list(range(len_txt))
        nums = cls.generate_keylist(len_txt, key)
        for idx in range(len_txt):
            try:
                new_nums.append(temp_num.pop(nums[idx] % len(temp_num)))
            except ZeroDivisionError:
                pass

        return new_nums

    @classmethod
    def xor_and_convert_to_bin(cls,txt,key):
        dict1,dict2 = cls.get_dicts(key)
        new_key = ''
        new_txt = ''

        for char in key:
            temp = bin(dict2[char])[2:]  
            while len(temp) < 8:
                temp = '0' + temp
            new_key +=  temp    
        
        for char in txt:
            temp = bin(dict2[char])[2:]  
            while len(temp) < 8:
                temp = '0' + temp
            new_txt +=  temp    

        final = ''
        for idx in range(len(new_txt)):
            final += '1' if new_txt[idx] == new_key[idx] else "0"

        shuffled_bytes = Block_Enc.split_to_parts(new_txt,8)
        return ''.join(dict1[int(block.bytes,2)] for block in shuffled_bytes)


    @classmethod
    def shuffle(cls, txt, key):
        new_txt = ''
        row_shifts = cls.generate_shuffle_list(len(txt), key)
        
        for idx in range(len(txt)):
            new_txt += txt[row_shifts[idx]]

        return new_txt

    @classmethod
    def un_shuffle(cls, txt, key):
        shifts = cls.generate_shuffle_list(len(txt), key)
        new_list = ['' for char in txt]
        for idx in range(len(shifts)):
            new_list[shifts[idx]] = txt[idx]
        return Enc.convert_to_str(new_list)
        

    @classmethod
    def convert_to_str(cls,listt):
        new_str = ''
        for char in listt:
            new_str+=char

        return new_str

    @classmethod
    def shuffle_bin(cls,txt,key):
        temp = txt 
        keys = list(cls.create_list(key,(64)*4))

        for idx in range(len(keys)):
            temp = cls.shuffle_helper(temp,keys[idx])
            temp = cls.xor_and_convert_to_bin(temp,keys[idx])

        return temp

    @classmethod
    def un_shuffle_bin(cls,txt,key):
        temp = txt 
        keys = list(cls.create_list(key,(64)*4))

        for idx in range(len(keys)):
            temp = cls.xor_and_convert_to_bin(temp,keys[len(keys)-1-idx])
            temp = cls.un_shuffle_helper(temp,keys[len(keys)-1-idx])

            

        return temp

    @classmethod
    def shuffle_helper(cls,txt,key):
        dict1,dict2 = cls.get_dicts(key)
        new_txt = ''
        for char in txt:
            temp = bin(dict2[char])[2:]  
            while len(temp) < 8:
                temp = '0' + temp
            new_txt +=  temp     

        shuffled_bytes =  Block_Enc.split_to_parts(cls.shuffle(new_txt,key),8)
        return ''.join(dict1[int(block.bytes,2)] for block in shuffled_bytes)

    @classmethod
    def un_shuffle_helper(cls,txt,key):
        dict1,dict2 = cls.get_dicts(key)
        new_txt = ''
        for char in txt:
            temp = bin(dict2[char])[2:]  
            while len(temp) < 8:
                temp = '0' + temp
            new_txt += temp

        shuffled_bytes =  Block_Enc.split_to_parts(cls.un_shuffle(new_txt,key),8)
        return ''.join(dict1[int(block.bytes,2)] for block in shuffled_bytes)

class Block:
    def __init__(self,bytes):
        self.bytes = bytes

    def mix(self,key):
        self.bytes = Enc.shuffle_bin(self.bytes,key)
    
    def un_mix(self,key):
        self.bytes = Enc.un_shuffle_bin(self.bytes,key)


class Block_Enc: 

    @classmethod
    def split_to_parts(cls, text,block_size = 16):
        blocks = []
        last_idx = 0
        for idx in range(len(text) // block_size):
            splitted_txt = text[idx * block_size : (idx + 1 ) * block_size]
            blocks.append(Block(splitted_txt))
            last_idx = idx

        txt =text[(last_idx + 1) * block_size + 1:]

        if txt != '':
            last_block  = Block(txt)
            blocks.append(last_block)

        return blocks

    @classmethod
    def connect_blocks(cls, blocks):
        result = ''

        for block in blocks:
            result += block.bytes
        return result

    @classmethod
    def xor_str(cls,str_1, str_2,dict_1, dict_2,enc=True):
        new_str = ""
        shift_num = 0
        for char in str_2:
            shift_num += dict_2[char]

        shift_num %= 64
        if enc:
            str_1 = Enc.shuffle(str_1,str_2)
            str_1 = cls.string_bit_shift(str_1,dict_1,dict_2, shift_num)

            for char_1,char_2 in zip(str_1, str_2):
                new_str += (dict_1[( dict_2[char_1] ^ dict_2[char_2] )])
        else :
            for char_1,char_2 in zip(str_1, str_2):
                new_str += (dict_1[( dict_2[char_1] ^ dict_2[char_2] )])
            
            new_str = cls.string_bit_shift(new_str,dict_1,dict_2, -shift_num)
            new_str = Enc.un_shuffle(new_str,str_2)
        # str_1.bytes = new_str
        return new_str
    @classmethod
    def mix_blocks(cls, blocks, key_list):

        for idx  in range(len(blocks)):
            blocks[idx].mix(key_list[idx])

        return cls.mixblock(blocks,key_list[-1])

    @classmethod
    def un_mix_blocks(cls, blocks, key_list):
        blocks = cls.unmixblock(blocks,key_list[-1])
        for idx  in range(len(blocks)):
            blocks[idx].un_mix(key_list[idx])

        return blocks

    @classmethod
    def string_bit_shift(cls,string,dict_1, dict_2,shift_num):
        num_list = [str(bin(dict_2[char]))[2:] for char in string]


        for idx in range(len(num_list)):
            if  len(num_list[idx]) < 8:
                diff = 8 - len(num_list[idx]) 
                adding = "".join(["0" for _ in range(diff)])
                adding += num_list[idx]
                num_list[idx] = adding
    
        byte_str = "".join(num_list)
        byte_str = cls.string_shift(byte_str,shift_num)


        byte_list =[]

        for idx in range(len(byte_str) // 8):
            byte_list.append(byte_str[idx * 8:(idx+1) * 8])
        
        return "".join([dict_1[int(byt,2)] for byt in byte_list])

    @classmethod
    def string_shift(cls,string,shift_num ):
        new_string = string[shift_num:]
        new_string += string[:shift_num]
        return new_string
        
    @classmethod
    def mixblock(cls,blocks,key):
        row_shifts = Enc.generate_shuffle_list(len(blocks), key)
        aux_list = blocks[:]

        for idx in range(len(blocks)):
            aux_list[idx] = blocks[row_shifts[idx]]
        
        return aux_list

    @classmethod
    def unmixblock(cls,blocks,key):
        row_shifts = Enc.generate_shuffle_list(len(blocks), key)
        aux_list = blocks[:]

        for idx in range(len(blocks)):
            aux_list[row_shifts[idx]] = blocks[idx] 

        return aux_list
        

