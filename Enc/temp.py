from operator import xor
from enc import Block_Enc as be
from enc import Block as b 
from enc import Enc as e

# block = b("qwertyuiopasdfghjklzxcvbnm")
# key = "test_key_123_11"
# d1,d2 = e.get_dicts(e.convert_to_hash(key))
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

blocks = be.split_to_parts("sadasdasdasdasd",2)
blocks_copy = blocks.copy()

print(blocks is blocks_copy)