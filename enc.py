from hashlib import sha256


class Enc:

    # creater a string that is as the size of the file from hashes using sha256
    @classmethod
    def create_list(cls, Key, size):
        if size <= 64:
            new_key = []
            new_key.append(Key)
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
    def create_file(cls, key, size):
        keys_list = cls.create_list(key, size * 5)
        with open('keys.txt', 'w') as temp:
            for key in keys_list:
                temp.write(key)

    """ takes the size of the text that to be encrypted  and takes the key to genrate the file (keys.txt) using the class
     method create_file adn then take  the  series of hashes and pass it to the nums classmethod"""
    @classmethod
    def generate_keylist(cls, txt_size, key):
        cls.create_file(key, txt_size)
        num_list = []
        with open('keys.txt', 'r') as keys:
            key = list(keys.read())

            for idx in range(1, int(len(key) // 5) + 1):
                if idx > len(key):
                    break

                else:
                    temp_list = key[(idx * 5) - 5:idx * 5]
                    num_list.append(cls.generate_nums(temp_list)) 

        return num_list

    """ takes  a list of len 5 and genrate a number from it to pass it back to  generate_keylist """
    @classmethod
    def generate_nums(cls, temp_list):
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
        keys = cls.generate_keylist(len(character_list), key)

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
                , 'ب', 'ي', 'س', 'ش', 'ئ', 'ء', 'ؤ', 'ر', 'ﻻ', 'ى', 'ة', 'و', 'ز', 'ظ']
    
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


