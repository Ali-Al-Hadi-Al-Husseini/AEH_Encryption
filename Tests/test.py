import matplotlib.pyplot as plt
import numpy as np
from AEH import AEH

path = str(input("Path:"))
key = str(input("key:"))
file = open(path, 'r')

text  = file.read()
file.close()

encrypted_text = AEH.Encrypt(text, key)
with open('encrypted.txt') as txt:
    txt.write(encrypted_text)
    

charcter_list = ["'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4',
                '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E',
                'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g',
                'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                'y', 'z', ' ', '\n', '…', '!', '’', '→', '‘', '“', '”', '{', '}', '"', '&', '—', '×',
                '–', '%', '#', 'ض', 'ص', 'ث', 'ق',
                'ف', 'غ', 'ع', 'ه', 'خ', 'ح', 'ج', 'د', 'ط', 'ك', 'م', 'ن', 'ت', 'ا', 'ل'
                , 'ب', 'ي', 'س', 'ش', 'ئ', 'ء', 'ؤ', 'ر', 'ﻻ', 'ى', 'ة', 'و', 'ز', 'ظ']

charcter_dict = {}
for char in charcter_list:
    charcter_dict[char] = 0

for line in encrypted_text:
    for char in line:
        charcter_dict[char] += 1

chacter_recurance = [value for value in charcter_dict.values()]


y_pos = np.arange(len(charcter_list))
plt.xticks(y_pos, charcter_list)
plt.bar(y_pos, chacter_recurance)
plt.show()


