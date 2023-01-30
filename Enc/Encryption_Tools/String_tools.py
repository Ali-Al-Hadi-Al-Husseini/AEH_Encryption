from numpy import empty


class String_tools:
    @classmethod
    def xor_str(cls,block, key,d1, d2):
        txt = block.bytes
        if len(txt) > len(key):
            raise ValueError('Text and key should be the same length in xor_str')

        xor_result = empty((len(txt)),dtype='<U2')

        for idx in range(len(txt)):
            xor_result[idx] = d1[ d2[txt[idx]] ^ d2[key[idx]]]

        result = ''.join(xor_result)
        block.bytes =  result 
        return result


    @classmethod
    def string_bit_shift(cls,string,dict_1, dict_2,shift_num,Encrypt = True):
        if type(string) != str or type(shift_num) != int: 
            raise TypeError("String should be str  and shiftnum should be int")

        num_list = [str(bin(dict_2[char]))[2:] for char in string]
        byte_length = 8


        for idx,num in enumerate(num_list):
            if  len(num) < byte_length:
                diff = byte_length - len(num) 
                adding = "0" * diff + num
                num_list[idx] = adding
    
        byte_str = "".join(num_list)
        
        if Encrypt:
            byte_str = cls.string_shift(byte_str,shift_num)
        else:
            byte_str = cls.string_un_shift(byte_str,shift_num)

        byte_list = empty((len(byte_str) // 8),dtype="<U9")

        for idx in range(len(byte_str) // 8):
            byte_list[idx] = byte_str[idx * 8:(idx+1) * 8]
        
        return "".join([dict_1[int(byt,2)] for byt in byte_list])


    @classmethod
    def string_shift(cls,string,shift_num ):
        shift_num %= 1 if len(string) < 1  else len(string)
        shift = len(string) - shift_num

        shifted_string = string[shift:] + string[:shift]

        return shifted_string


    @classmethod
    def string_un_shift(cls,string,shift_num):
        shift_num %= 1 if len(string) < 1 else len(string)
        
        unshifted_string = string[shift_num:] + string[:shift_num] 

        return unshifted_string