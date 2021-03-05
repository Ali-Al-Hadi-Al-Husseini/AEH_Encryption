from hashlib import sha256
from os import remove

    
class Enc:

    # creater a string that is as the size of the file from hashes using sha256
    @classmethod
    def create_list(cls,Key,size):
        if size <= 64:
            new_key = []
            new_key.append(sha256(Key.encode()).hexdigest())
            return new_key

        else:
            new_keys = []
            new_list = cls.create_new_list( cls.create_list1( Key,(size // 2)))
            new_keys.extend( new_list)
            return new_keys

    #this method take one parameter (hash as a string) and then returns the hashs of the two halfs of the key
    @classmethod
    def split_and_hash(cls,key):
        half_key = int(len(key) /2) + 1
        return list((sha256(key[half_key:].encode()).hexdigest(),sha256(key[:half_key].encode()).hexdigest()))
    
    #takes a list of hashes and return a twice as big list from spliting anf hashing each hash
    @classmethod
    def create_new_list(cls,keys):
        new_keys = []
        for key in keys:
            new_keys.extend( cls.split_and_hash(key))

        return new_keys

    #write the  generated list from create_new_list in a file called keys.txt
    @classmethod
    def  create_file(cls,key,size):
        keys_list = cls.create_list(key,size * 5)
        with open('keys.txt', 'w') as temp:
            for key in keys_list:
                temp.write(key)
                
    """ takes the size of the text that to be encrypted  and takes the key to genrate the file (keys.txt) using the class
     method create_file adn then take  the  series of hashes and pass it to the nums classmethod"""
    @classmethod
    def generate_keylist(cls,txt_size,key):
        cls.create_file(key, txt_size)
        num_list = []
        with open('keys.txt','r') as keys:
            key = list(keys.read())
            
            for idx in range(1, int(len(key) // 5) + 1):
                if idx > len(key):
                    break

                else:
                    temp_list = key[(idx * 5) - 5:idx * 5]
                    num = cls.nums(temp_list)
                    num_list.append((num % 83) + 39)
            
        remove('keys.txt')
        return num_list
    
    """ takes  a list of len 5 and genrate a number from it to pass it back to  generate_keylist """
    @classmethod
    def nums(cls,temp_list):
        #checks to see if ther are any letter in the list and then change it to numbers 
        for idx in range(len(temp_list)):
            if type(temp_list[idx]) == str:
                temp_list[idx] = ord(temp_list[idx])
                
        #this block genrates new number from the five number in the temp_list
        num2 = int(((( temp_list[1] ** temp_list[3]) + temp_list[2]) * temp_list[4] ) // temp_list[0])
        num3 = int((7 ** (temp_list[0] + temp_list[1] + temp_list[2] + temp_list[3] + temp_list[4])) // 3)
        num1 = 0
        
        try:
            num1 += int(((( temp_list[2] ** temp_list[1]) + temp_list[0]) * temp_list[4] ) // temp_list[3])
            #in cases where temp_list[3] can be zero so thats why we used try/execpt here 
            
        except ZeroDivisionError:
            #provides two alternative number if num1 has an error
            try :
                num1 = num2

            except ZeroDivisionError:
                """num3 cann't have an error because it uses only addtion it can only be 0 if all the i
                tems in temp_list is zero which is to rare to happen """
                
                num1 = num3    
        if num1 != 0:
            
            return num1

        else:
            print('this key is not safe enough') 
            return None
       
    # converts  a list which is normally passed from the class method generate_new_dicts
    @classmethod
    def convert_to_dict(cls,character_list):
        dict1 = {}

        for i in len(character_list):
            dict1[i] = character_list[i]

        return dict1
    
    # returns a new dict where the keys are the value and vice versa
    @classmethod
    def reverse_dict(cls,dict1):
        new_dict = {}

        for key, value in dict1:
            new_dict[value] = key

        return new_dict
    
    """take a key and generates a new list with different order  of the letters (changes the index of each letter and give a new_list)
    which means every key have different order of letter which makes it a bit harder to crack it """
    @classmethod
    def generate_new_dict(cls, key):
        character_list = ["'", '(', ')', '*', '+', ',', '-', '.', '/', '0',
                          '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=',
                          '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                          'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
                          'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd',
                          'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                          'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']

        new_character_list = []
        keys = cls.generate_keylist(len(character_list), key)
        for idx in range(len(character_list)):
            new_character_list.append(character_list.pop(
                keys[idx] % len(character_list)))

        return new_character_list
    # changes the order of each letter in the txt  passed which give an exrtra layer of protection
    @classmethod
    def matrix_manipultion(cls,txt, key):
    new_nums = []
    nums = []
    temp_num = [1, 3, 0, 2]
    for idx in range(1, len(key) // 8):
        nums = key[(idx - 1) * 8: idx * 8 - 1]
        try:
            x = cls.num(nums) % (len(temp_num))
            new_nums.append(temp_num.pop(x))
        except ZeroDivisionError:
            pass
    return new_nums

    @classmethod
    def num(cls,nums):
        new_num = 0
        for idx in range(len(nums)):
            new_num += ord(nums[idx])

        return new_num
    # this part need to be wired


    
    
    
