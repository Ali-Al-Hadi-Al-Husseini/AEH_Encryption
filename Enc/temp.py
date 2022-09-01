from enc import Block_Enc as be
from enc import Block as b 
from enc import Enc as e

# block = b("qwertyuiopasdfghjklzxcvbnm")
key = "test_key_123_11"
d1,d2 = e.get_dicts(e.convert_to_hash(key))
# t1 = "qwerty"
# t2 = "asdrty"
# chars = []

# from AEH import AE
# en = AE.Block_Encryption('asdssadasdasdasdasddasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdasdsasdasdasdasdsaada',key)
# print(en)
# print(AE.Block_Decryption(en,key))
# x = ((bin(d2['n'])[2:]))
# x1 = (((bin(d2['a'])[2:])))
# nd= ''.join(['0' for _ in range(8-len(x))])
# nw = nd + x
# print(nw)

# r1 = d2['a']
# r2 = d2['n']
# r = r1 ^ r2
# print(r1)
# print(r)
# print(d1[r ^ r2])
# print(r2 ^ r)


# def func(t1,t2,d1,d2):
#     if len(t1) != len(t2):
#         raise ValueError('Text and key should be the same length in xor_str')
#     res = [None for _ in t1]
#     j = 0
#     for idx in range(len(t1)):
#         res[j] = d1[ d2[t1[idx]] ^ d2[t2[idx]]]
#         j += 1

#     return ''.join(res)

# res = (func('abc','mnb',d1,d2))
# print(res)
# print((func(res,'mnb',d1,d2)))

# blocks = be.split_to_parts("sadasdasdasdasd",2)
# blocks_copy = blocks.copy()

# print(blocks is blocks_copy)

# string = "abcd"

# new_string = be.string_bit_shift('hola_myamigo',d1,d2,2)
# print('678912345' == new_string)

# string = "as dsadasds adasd asdsadasda sdasd asdas das dasd asdlj glsdjgodsiagh kJSDGAASDG LAKGALKD G HADSLKFHDSKUGFSDLKJgb SDLKGNREKUHT ERAKUGTH ERSIUG HREPIU VHERPIU GERKJHG ERP KJ bokjbdnogfdi"

# bytes_strings = be.string_shift(string,20)
# print(be.string_un_shift(bytes_strings,20))
# test_cases_success = [
#         ('abcasd adssad',5),
#         ('1234561010789',3),
#         ('hola_myam123igo',19),
#         ('',3),
#         ("mamamia gola tensioni",100)
# ]
# test_cases_error = [
#             (123442,124),
#             ('12345','as'),
#             (1234,'ds')
# ]

# # for txt,shift in test_cases_success:
# #     result = be.string_bit_shift(txt,self.dict1,self.dict2,shift)
# #     if result != "":
# #         self.assertNotEqual(result,txt)
# #     self.assertEqual(be.string_bit_shift(result,self.dict1,self.dict2,shift,False),txt)

# for txt,shift in test_cases_error:
#     be.string_bit_shift(txt,d1,d2,shift)

# def get_nearist_2_power(num):
#     curr_num = 2
#     counter = 0
#     while curr_num < num:
#         curr_num *= 2
#         counter += 1
#     return counter
    
# test_cases = [
#             (1, 0),#since 2 ** 0 == 1
#             (55,6),#since 2 ** 6 == 64 which is the nearset to 55
#             (1000,10),
#             (110_000,17),
#             (1_000_000_000,1_073_741_824)
# ]

# for num, expected_result in test_cases:
#     assert expected_result == get_nearist_2_power(num)

# ke = e.convert_to_hash("ASdsad")
# print(len(e.create_hash_list(ke,250,1)))
# print(len(e.generate_keylist(250,'afffmlkhs h')))
from random import randrange

# for _ in range(10000):
#     x = randrange(0,10000)
#     print('===',x,'===')
#     e.generate_shuffle_list(6647,"asdasbikhalfhasfhasnufhas")

print(len(e.generate_keylist(6647, "asdasbikhalfhasfhasnufhas")))
print("lalalalal")
# print(e.generate_shuffle_list(20,"asdsadasdsadasdasdsad"))