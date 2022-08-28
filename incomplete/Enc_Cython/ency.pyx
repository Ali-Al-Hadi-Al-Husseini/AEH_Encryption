from hashlib import new, sha256
from threading import Thread
from multiprocessing import Process
import cython


# creater a string that is as the size of the file from hashes using sha256

def create_list( str Key, int size, int add_to_half = 1):
    if size <= 64:
        new_key = [Key]
        return new_key

    else:
        new_keys = []
        new_list =  create_new_list( create_list(Key, (size // 2),add_to_half))
        new_keys.extend(new_list)
        return new_keys

# this method take one parameter (hash as a string) and then returns the hashs of the two halfs of the key
    
def split_and_hash( char*  key, int add_to_half = 1):
    cdef int half_key = int(len(key) / 2) + add_to_half
    return list((sha256(key[half_key:].encode()).hexdigest(), sha256(key[:half_key].encode()).hexdigest()))

# takes a list of hashes and return a twice as big list from spliting anf hashing each hash
    
def create_new_list(  list keys):
    new_keys = []

    for key in keys:
        new_keys.extend( split_and_hash(key))

    return new_keys

# write the  generated list from create_new_list in a file called keys.txt
    
def create_hash_list( str key,int  size,int add_to_half = 1):
    keys_list =  create_list(key, size * 5,add_to_half)
    cdef char* result = ""
    for key in keys_list:
        result += key
    return list(result)

""" takes the size of the text that to be encrypted  and takes the key to genrate the file (keys.txt) using the class
    method create_hash_list adn then take  the  series of hashes and pass it to the nums classmethod"""
    
cdef list generate_keylist(  int txt_size, char* key, int  add_to_half = 1, char* case="NONE"):
    key =  create_hash_list(key, txt_size,add_to_half)
    cdef int len_txt = int(len(key) // 5) + 1
    cdef int[len_txt] num_list
    
    for idx in range(1, int(len(key) // 5) + 1):
        if idx > len(key):
            break

        else:
            temp_list = key[(idx * 5) - 5  :idx * 5]
            num_list.append[idx] = ( generate_nums(temp_list,case)) 

    return num_list

""" takes  a list of len 5 and genrate a number from it to pass it back to  generate_keylist """
    
cdef int generate_nums( int[] temp_list, char* Case='NONE'):
    # checks to see if ther are any letter in the list and then change it to numbers
    for idx in range(len(temp_list)):
        if type(temp_list[idx]) == str:
            temp_list[idx] = ord(temp_list[idx])

    # this block genrates new number from the five number in the temp_list
    cdef int len_chars = len( get_character_list())
    cdef int num1 = 0

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
    
def  convert_to_dict( list character_list):
    dict1 = {}

    for i in range(len(character_list)):
        dict1[i] = character_list[i]

    return dict1

# returns a new dict where the keys are the value and vice versa
    
def reverse_dict(  dict1):
    new_dict = {}

    for key, value in dict1.items():
        new_dict[value] = key
    return new_dict

"""take a key and generates a new list with different order  of the letters (changes the index of each letter and give a new_list)
which means every key have different order of letter which makes it a bit harder to crack it """
    
def generate_character_list(  char* key):
    character_list =  get_character_list()
    cdef int keys_size = int(len(key) // 5) + 1
    cdef int[256] new_character_list 
    cdef int[keys_size] keys =  generate_keylist(len(character_list), key,'A')

    cdef int len_char_list = len(character_list)

    for idx in range(len(character_list)):
        new_character_list.append(character_list[(
            keys[idx] % len_char_list)])
        len_char_list -= 1

    return new_character_list

    
def get_dicts(  key,character_list = None):
    if character_list is None:
        character_list =  generate_character_list(key)
    dict1 =  convert_to_dict(character_list)
    dict2 =  reverse_dict(dict1)

    return dict1, dict2

    

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

    

cdef str convert_to_hash( txt):
    return sha256(txt.encode()).hexdigest()

    
def generate_shuffle_list( int len_txt,str key):
    cdef int[len_txt] new_nums 
    nums = []
    cdef int len_num = int(len(key) // 5) + 1
    cdef int[len_txt] temp_num = list(range(len_txt))
    cdef int[len_num] nums =  generate_keylist(len_txt, key)

    for idx in range(len_txt):
        try:
            new_nums[idx] = (temp_num.pop(nums[idx] % len(temp_num)))
        except ZeroDivisionError:
            pass

    return new_nums


    

cdef str shuffle(  char* txt,char* key):
    new_txt = ''
    cdef int len_num = int(len(key) // 5) + 1
    cdef int[len_num] row_shifts =  generate_shuffle_list(len(txt), key)
    
    for idx in range(len(txt)):
        new_txt += txt[row_shifts[idx]]

    return new_txt

    
def  un_shuffle( str txt,str key):
    cdef int len_num = int(len(key) // 5) + 1
    cdef int[len_num] shifts =  generate_shuffle_list(len(txt), key)
    cdef int[len(txt)]new_list = ['' for charr in txt]

    for idx in range(len(shifts)):
        new_list[shifts[idx]] = txt[idx]

    return Enc.convert_to_str(new_list)
    

    
def convert_to_str( list listt):
    return "".join(listt)

    
def shuffle_bin( str txt,str key):
    cdef str temp = txt 
    cdef list keys = list( create_list(key,(64)*4))
    
    for idx in range(len(keys)):
        temp =  shuffle_helper(temp,keys[idx])
    return temp

    
def un_shuffle_bin( txt,key):
    temp = txt 
    keys = list( create_list(key,(64)*4))

    for idx in range(len(keys)):
        temp =  un_shuffle_helper(temp,keys[len(keys)-1-idx])
    return temp

    
def  shuffle_helper( str txt,str key):
    dict1,dict2 =  get_dicts(key)
    cdef str new_txt = ''

    for char in txt:
        temp = bin(dict2[char])[2:]  
        while len(temp) < 8:
            temp = '0' + temp
        new_txt +=  temp     

    shuffled_bytes = split_to_parts( shuffle(new_txt,key),8)
    return ''.join(dict1[int(block.bytes,2)] for block in shuffled_bytes)

    
def un_shuffle_helper( txt,key):
    dict1,dict2 =  get_dicts(key)
    new_txt = ''
    for char in txt:
        temp = bin(dict2[char])[2:]  
        while len(temp) < 8:
            temp = '0' + temp
        new_txt += temp

    shuffled_bytes =  split_to_parts( un_shuffle(new_txt,key),8)
    return ''.join(dict1[int(block.bytes,2)] for block in shuffled_bytes)

class Block:
    def __init__(self,bytes):
        self.bytes = bytes

    def mix(self,key):
        self.bytes =   shuffle_bin(self.bytes,key)
    
    def un_mix(self,key):
        self.bytes =   un_shuffle_bin(self.bytes,key)
    
    def __len__(self):
        return len(self.bytes)

     
def split_to_parts(  text,block_size = 16):
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

    
def connect_blocks(  blocks):
    result = ''

    for block in blocks:
        result += block.bytes
    return result

    
def xor_str( block, key,dict_1, dict_2,enc=True):
    new_str = ""
    shift_num = 0
    for char in key:
        shift_num += dict_2[char]

    shift_num %= 64
    if enc:
        str_1 =   shuffle(block.bytes,key)
        str_1 =  string_bit_shift(str_1,dict_1,dict_2, shift_num)

        for char_1,char_2 in zip(str_1, key):
            new_str += (dict_1[( dict_2[char_1] ^ dict_2[char_2] )])
    else :
        for char_1,char_2 in zip(block.bytes, key):
            new_str += (dict_1[( dict_2[char_1] ^ dict_2[char_2] )])
        
        new_str =  string_bit_shift(new_str,dict_1,dict_2, -shift_num)
        new_str =   un_shuffle(new_str,key)
        
    # block.bytes = new_str

    
def mix_blocks(  blocks, key_list):

    for idx  in range(len(blocks)):
        blocks[idx].mix(key_list[idx])

    return  mixblock(blocks,key_list[-1])

    
def un_mix_blocks(  blocks, key_list):
    blocks =  unmixblock(blocks,key_list[-1])
    for idx  in range(len(blocks)):
        blocks[idx].un_mix(key_list[idx])

    return blocks

    
def mix_blocks_process(  blocks, key_list):
    processs = []
    for idx  in range(len(blocks)):
        process = Process(target=blocks[idx].mix,args=(key_list[idx],))
        process.start()
        processs.append(process)
    
    for process in processs:
        process.join()

    return  mixblock(blocks,key_list[-1])

    
def un_mix_blocks_process(  blocks, key_list):
    processs = []
    blocks =  unmixblock(blocks,key_list[-1])
    for idx  in range(len(blocks)):
        process = Process(target=blocks[idx].mix,args=(key_list[idx],))
        process.start()
        processs.append(process)
        

    for process in processs:
        process.join()

    return blocks

    
def string_bit_shift( string,dict_1, dict_2,shift_num):
    num_list = [str(bin(dict_2[char]))[2:] for char in string]


    for idx in range(len(num_list)):
        if  len(num_list[idx]) < 8:
            diff = 8 - len(num_list[idx]) 
            adding = "".join(["0" for _ in range(diff)])
            adding += num_list[idx]
            num_list[idx] = adding

    byte_str = "".join(num_list)
    byte_str =  string_shift(byte_str,shift_num)


    byte_list =[]

    for idx in range(len(byte_str) // 8):
        byte_list.append(byte_str[idx * 8:(idx+1) * 8])
    
    return "".join([dict_1[int(byt,2)] for byt in byte_list])

    
def string_shift( string,shift_num ):
    new_string = string[shift_num:]
    new_string += string[:shift_num]
    return new_string
    
    
def mixblock( blocks,key):
    row_shifts =   generate_shuffle_list(len(blocks), key)
    aux_list = blocks[:]

    for idx in range(len(blocks)):
        aux_list[idx] = blocks[row_shifts[idx]]
    
    return aux_list

    
def unmixblock( blocks,key):
    row_shifts =   generate_shuffle_list(len(blocks), key)

    aux_list = blocks[:]

    for idx in range(len(blocks)):
        aux_list[row_shifts[idx]] = blocks[idx] 

    return aux_list

    
def xor_blocks( blocks,key_list,dict1,dict2,enc=True):
    threads = []
    for idx  in range(len(blocks)):
        thread = Thread(target= xor_str,args=(blocks[idx],key_list[idx],dict1,dict2,enc))
        thread.daemon = True
        threads.append(thread)
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


# txt = "ali ishere"
# key = 'ls'

# def func(txt,key):
#     dict1,dict2 = Enc.get_dicts(key)
#     new_txt = ''
#     for char in txt:
#         new_txt += bin(dict2[char])[2:]
#     return new_txt

# x =func(txt,key)
# print(x)
# print(Enc.un_shuffle(Enc.shuffle(x,key),key))
# x = [0,1,2,3,4,5,6,7,8,9]
# key = Enc.convert_to_hash("adsada")
# x= Block_Enc.mixblock(x,key)
# print(x)
# x = Block_Enc.unmixblock(x,key)
# print(x)
