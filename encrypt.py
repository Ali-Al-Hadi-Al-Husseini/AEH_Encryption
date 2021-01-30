# 33 --> 126
import numpy as np
from hashlib import sha256
from enc import enc

def AEH(thelist,key):
    coded  = []
    new_txt = ''
    new_key = str(sha256(key.encode()).hexdigest())
    print(new_key)
    print(len(new_key))
    for i in range(len(thelist)):
       x = ord(thelist[i])+ord(new_key[i])
       coded.append(x)

    
    for i in coded:
        x = int(i % 93) + 33
        new_txt = new_txt + str(chr(x+1))

    return new_txt
def AEHD(txt,key):
    newkey = str(sha256(key.encode()).hexdigest())
    new_txt = ''
    for i in range(len(txt)):
        x = ord(txt[i])-ord(newkey[i])
        new_txt.append(chr(x))
    

print(AEH('Hellolantslktbgs','trialhnf'))
