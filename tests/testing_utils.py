from ..Enc.enc import Block as b

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

def copy_blocks(blocks):
    blocks_copy = [None for block in blocks]

    for idx in range(len(blocks)):
        curr_block = blocks[idx] 
        new_block = b(curr_block.bytes)
        blocks_copy[idx] = new_block

    return blocks_copy