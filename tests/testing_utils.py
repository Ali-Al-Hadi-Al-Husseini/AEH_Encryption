# def contains_the_same_letters(txt1,txt2):
#     if len(txt1) != len(txt2) : return False

#     txt1_chars_counter = {}
#     txt2_chars_counter = {}


#     for char_ in txt1:
#         if char_ in  txt1_chars_counter:
#             txt1_chars_counter[char_] += 1
#         else:
#             txt1_chars_counter[char_] = 1

#     for char_ in txt2:
#         if char_ in  txt2_chars_counter:
#             txt2_chars_counter[char_] += 1
#         else:
#             txt2_chars_counter[char_] = 1
    
#     for char_ in txt1_chars_counter:
#         if txt1_chars_counter[char_] == txt2_chars_counter[char_]:
#             continue
#         return False
#     return True

    # def test_contains_the_same_letters_true(self):
    #     same_texts = [
    #         ("qwertyuio",'oiuytrewq'),
    #         ('qwertyuiop','poiuytrewq'),
    #         ('1234567890','0987654321'),
    #         ('asdfghjkl','lkjhgfdsa'),
    #         ('zzxxccvvbbnnmm','mmnnbbvvccxxzz')
    #     ]
    #     for txt in same_texts:
    #         self.assertTrue(contains_the_same_letters(txt[0],txt[1]))

    # def test_contains_the_same_letters_false(self):
    #     same_texts = [
    #         ("qwertyu2io",'oiuytrewq'),
    #         ('qwertyuio4p','poiuytrewq'),
    #         ('12345617890','0987654321'),
    #         ('asdfgh4jkl','lkjhgfdsa'),
    #         ('zzxxccfvvbbnnmm','mmnnbbvvccxxzz')
    #     ]
    #     for txt in same_texts:
    #         self.assertFalse(contains_the_same_letters(txt[0],txt[1]))

def same_but_splited(txt,splited_parts):
    len_splited_parts = len(''.join(splited_parts))
    if len_splited_parts != len(txt):return False

    return txt == ''.join(splited_parts)

def remove_modulo(txt:str) -> str:
    txt = list(txt)


    while txt[-1] == '%':
        txt.pop()
        if len(txt) == 0 :
            break
    
    return ''.join(txt)

def same_but_mixed(List, mixed_list):
    if len(List) != len(mixed_list): return False
    
    list_set = set(List)

    for item in mixed_list:
        if item not in list_set:
            return False
    return True