from hashlib import sha256
from os import remove

    
class Enc:

    # creater a string that is as the size of the file
    @classmethod
    def create_list1(cls,Key,size):
        if size <= 64:
            new_key = []
            new_key.append(sha256(Key.encode()).hexdigest())
            return new_key

        else:
            new_keys = []
            new_list = cls.create_new_list( cls.create_list1( Key,(size // 2)))
            new_keys.extend( new_list)
            return new_keys

    #this method take one parameter (hash as a string) and then returns the hash of the half of the key
    @classmethod
    def split_and_hash(cls,key):
        half_key = int(len(key) /2) + 1
        return list((sha256(key[half_key:].encode()).hexdigest(),sha256(key[:half_key].encode()).hexdigest()))

    @classmethod
    def create_new_list(cls,keys):
        new_keys = []
        for key in keys:
            new_keys.extend( cls.split_and_hash(key))

        return new_keys

    #write the last keys the keys.txt file
    @classmethod
    def  create_file(cls,key,size):
        keys_list = cls.create_list(key,size)
        with open('keys.txt', 'w') as temp:
            for key in keys_list:
                temp.write(key)
    @classmethod
    def create_list(cls,key,size):
        return cls.create_list1(key,size*5)


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
                    num_list.append((num % 83) +39)
            
        remove('keys.txt')
        return num_list 
    @classmethod
    def compare(cls,num):
        if num % 2 == 0:
            num = num*7
        elif  (num % 81 ) <= 34:
            num = 36 * num
        else:
            num = ((12 * num) * 7)
        return num

    @classmethod
    def nums(cls,temp_list):

        for idx in range(len(temp_list)):
            if type(temp_list[idx]) == str:
                temp_list[idx] = ord(temp_list[idx])

        num2 = int(((( temp_list[1] ** temp_list[3]) + temp_list[2]) * temp_list[4] ) // temp_list[0])
        num3 = int((7 ** (temp_list[0] + temp_list[1] + temp_list[2] + temp_list[3] + temp_list[4])) // 3)
        num1 = 0
        try:
            num1 += int(((( temp_list[2] ** temp_list[1]) + temp_list[0]) * temp_list[4] ) // temp_list[3])
                        
        except ZeroDivisionError:
            try :
                num1 = num2

            except ZeroDivisionError:
                num1 = num3    
        if num1 != 0:
            return num1

        else:
            print('this key is not safe enough') 
            return None
        
   @classmethod
    def get_dicts(cls):
        dict1 = {0: "'", 1: '(', 2: ')', 3: '*', 4: '+', 5: ',', 6: '-', 7: '.', 8: '/', 9: '0', 10: '1', 11: '2', 12: '3', 13: '4', 14: '5', 15: '6', 16: '7', 17: '8', 18: '9', 19: ':', 20: ';', 21: '<', 22: '=', 23: '>', 24: '?', 25: '@', 26: 'A', 27: 'B', 28: 'C', 29: 'D', 30: 'E', 31: 'F', 32: 'G', 33: 'H', 34: 'I', 35: 'J', 36: 'K', 37: 'L', 38: 'M', 39: 'N', 40: 'O', 41: 'P', 42: 'Q', 43: 'R', 44: 'S', 45: 'T', 46: 'U', 47: 'V', 48: 'W', 49: 'X', 50: 'Y', 51: 'Z', 52: '[', 53: '\\', 54: ']', 55: '^', 56: '_', 57: '`', 58: 'a', 59: 'b', 60: 'c', 61: 'd', 62: 'e', 63: 'f', 64: 'g', 65: 'h', 66: 'i', 67: 'j', 68: 'k', 69: 'l', 70: 'm', 71: 'n', 72: 'o', 73: 'p', 74: 'q', 75: 'r', 76: 's', 77: 't', 78: 'u', 79: 'v', 80: 'w', 81: 'x', 82: 'y', 83: 'z', 84: ' '} 
        dict2 = {"'": 0, '(': 1, ')': 2, '*': 3, '+': 4, ',': 5, '-': 6, '.': 7, '/': 8, '0': 9, '1': 10, '2': 11, '3': 12, '4': 13, '5': 14, '6': 15, '7': 16, '8': 17, '9': 18, ':': 19, ';': 20, '<': 21, '=': 22, '>': 23, '?': 24, '@': 25, 'A': 26, 'B': 27, 'C': 28, 'D': 29, 'E': 30, 'F': 31, 'G': 32, 'H': 33, 'I': 34, 'J': 35, 'K': 36, 'L': 37, 'M': 38, 'N': 39, 'O': 40, 'P': 41, 'Q': 42, 'R': 43, 'S': 44, 'T': 45, 'U': 46, 'V': 47, 'W': 48, 'X': 49, 'Y': 50, 'Z': 51, '[': 52, '\\': 53, ']': 54, '^': 55, '_': 56, '`': 57, 'a': 58, 'b': 59, 'c': 60, 'd': 61, 'e': 62, 'f': 63, 'g': 64, 'h': 65, 'i': 66, 'j': 67, 'k': 68, 'l': 69, 'm': 70, 'n': 71, 'o': 72, 'p': 73, 'q': 74, 'r': 75, 's': 76, 't': 77, 'u': 78, 'v': 79, 'w': 80, 'x': 81, 'y': 82, 'z': 83, ' ': 84}
        return dict1, dict2
    #this part is not doe yet
    @classmethod
    def generate_dicts(cls,key):
        #this is not doneyet but this should generate new distribution key value pair in the dictionaries 
        pass
    @classmethod
    def convert_to_dict(cls,character_list):
        dict1 = {}

        for i in len(character_list):
            dict1[i] = character_list[i]

        return dict1
       
    @classmethod
    def reverse_dict(cls,dict1):
        new_dict = {}

        for key, value in dict1:
            new_dict[value] = key

        return new_dict

    @classmethod
    def generate_dict(key):
        character_list = ["'", '(', ')', '*', '+', ',', '-', '.', '/', '0',
                          '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=',
                          '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                          'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
                          'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd',
                          'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                          'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']
        return character_list
    #till hear is now finished yet
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


    
    
    
