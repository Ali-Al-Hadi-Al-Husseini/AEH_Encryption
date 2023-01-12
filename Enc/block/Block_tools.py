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

