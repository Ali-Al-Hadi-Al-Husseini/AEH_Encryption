from Encryption_Tools.String_tools import String_tools
from Encryption_Tools.keys_tools import Keys
from Encryption_Tools.Dict_tools import Dict_Tools
from multiprocessing import Process

from numpy import empty

class Block:
    def __init__(self,bytes):
        self.bytes = bytes

    def mix(self,key):
        self.bytes = Shuffle.shuffle_bin(self.bytes,key)


    def un_mix(self,key):
        self.bytes = Shuffle.un_shuffle_bin(self.bytes,key)
    
    def __len__(self):
        return len(self.bytes)

class Block_Tools:

    @classmethod
    def split_to_parts(cls, text,block_size = 16):
        blocks = []
        last_idx = 0

        for idx in range(len(text) // block_size):
            splitted_txt = text[idx * block_size : (idx + 1 ) * block_size]
            blocks.append(Block(splitted_txt))
            last_idx = idx

        txt =text[(last_idx + 1) * block_size:]

        if txt != '':
            last_block  = Block(txt)
            blocks.append(last_block)

        return blocks

    @classmethod
    def connect_blocks(cls, blocks):
        return ''.join([block.bytes for block in blocks])

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
    def mixblock(cls,blocks,key):
        row_shifts = Shuffle.generate_shuffle_list(len(blocks), len(blocks), key)
        aux_list = blocks[:]

        for idx in range(len(blocks)):
            aux_list[idx] = blocks[row_shifts[idx]]
        
        return aux_list


    @classmethod
    def unmixblock(cls,blocks,key):
        row_shifts = Shuffle.generate_shuffle_list(len(blocks), len(blocks), key)

        aux_list = blocks[:]

        for idx in range(len(blocks)):
            aux_list[row_shifts[idx]] = blocks[idx] 

        return aux_list


    @classmethod
    def xor_blocks(cls,blocks,key_list,dict1,dict2):
        for idx  in range(len(blocks)):
            String_tools.xor_str(blocks[idx],key_list[idx],dict1,dict2)



    @classmethod
    def mix_blocks_process(cls, blocks, key_list):
        processs = []
        for idx  in range(len(blocks)):
            process = Process(target=blocks[idx].mix,args=(key_list[idx],))
            process.start()
            processs.append(process)
        
        for process in processs:
            process.join()

        return cls.mixblock(blocks,key_list[-1])

    @classmethod
    def un_mix_blocks_process(cls, blocks, key_list):
        processs = []
        blocks = cls.unmixblock(blocks,key_list[-1])
        for idx  in range(len(blocks)):
            process = Process(target=blocks[idx].mix,args=(key_list[idx],))
            process.start()
            processs.append(process)
            

        for process in processs:
            process.join()

        return blocks

    @classmethod
    def xor_blocks_procsess(cls,blocks,key_list,dict1,dict2):
        processs = []
        for idx  in range(len(blocks)):
            process = Process(target=String_tools.xor_str,args=(blocks[idx],key_list[idx],dict1,dict2))
            process.start()
            processs.append(process)
            

        for process in processs:
            process.join()

