from hashlib import sha256
class Enc:
        
    @classmethod
    def split_and_hash(cls, key):
        half_key = int(len(key) / 2) + 1
        return list((sha256(key[half_key:].encode()).hexdigest(), sha256(key[:half_key].encode()).hexdigest()))
    
    @classmethod
    def split_(cls,te,num=16):
        new = []
        len_te = len(te)
        mod_te = len_te % num
        

        for idx in range(int(len_te/num)):
            new.append(Matrix(te[idx*num: (idx+1)*num]))

        if  mod_te != 0:
            temp_list = te[len_te - mod_te :]
            new.append(Matrix(temp_list))
        return new

    @classmethod 
    def mix(cls, txt, key):
        txt_list = cls.split_(txt,16)

        for i in range(len(txt_list)):
            mat = Matrix(txt_list[i])
            mat.mix(key)
            txt_list[i] = mat.stringfy()

        return Matrix(txt_list).stringfy()
    @classmethod
    def get_layers(cls,len_txt):
        layers = 1
        while len_txt > 16:
            len_txt /= 16
            layers+=1
        return layers

    @classmethod
    def matricify(cls,txt):
        layers = cls.get_layers(len(txt))
        for i in range(layers):
            txt = cls.split_(txt,16)
        return Matrix(txt)


class Matrix:
    def __init__(self,txt):
        self.matrix = self.convert_to_matrix(txt)
        

    def convert_to_matrix(self ,txt):
        mat = [
            [],
            [],
            [],
            []
        ]
        row = 0
        for char in txt :
            if len(mat[row]) >= 4:
                row += 1
            mat[row].append(char)
            

        return mat


    def shift_rows(self, key):
        new_matrix = []
        row_shifts = self.matrix_manipultions(key)
        
        for num_row in range(len(self.matrix)):
            new_matrix.append(self.matrix[row_shifts[num_row]])

        self.matrix = new_matrix


    def get_matrix(self):
        return list(self.matrix)


    def shift_colunms(self, key):
        new_matrix = [[],
                      [],
                      [],
                      []]
        col_shifts = self.matrix_manipultions(key)

        for num_row in range(len(self.matrix)):
            for col in range(len(self.matrix[num_row])):
                new_matrix[num_row].append(self.matrix[num_row][col_shifts[col]])
        self.matrix = new_matrix

    ##NEEED TO BE FIXED TO MUCH IRETION
    def matrix_manipultions(self, key):
        new_nums = []
        nums = []
        temp_num = [1, 3, 0, 2]

        for idx in range(1, len(key) // 8):
            nums = key[(idx - 1) * 8: idx * 8 - 1]
            try:
                x = self.num(nums) % (len(temp_num))
                new_nums.append(temp_num.pop(x))
            except ZeroDivisionError:
                pass
        return new_nums

    def num(self, nums):
        new_num = 0

        for idx in range(len(nums)):
            new_num += ord(nums[idx])

        return new_num

    def mix(self,key):
        key_1, key_2 = Enc.split_and_hash(key)


        self.shift_rows(key_2)
        self.shift_colunms(key_1)


    def un_shift_colunms(self,key):
        col_shifts = self.matrix_manipultions(key)
        new_mat = []
        
        for row in (self.matrix):
            new_mat.append(self.un_shift_list(row,col_shifts))

        self.matrix = new_mat

    def un_shift_list(self,arr,shifts):
        new_list = ['','','','']
        for idx in range(len(shifts)):
            new_list[shifts[idx]] = arr[idx]
        return new_list

    def un_shift_rows(self,key):
        row_shifts = self.matrix_manipultions(key)
        new_mat = [[],
                   [],
                   [],
                   [],]
        for idx in range(len(row_shifts)):
            new_mat[row_shifts[idx]] =  self.matrix[idx]
        self.matrix = new_mat
        
    def un_mix(self,key):
        key_1 ,key_2 = Enc.split_and_hash(key)
    

        self.un_shift_colunms(key_1)
        self.un_shift_rows(key_2)
        
    def print(self):
        for row in self.matrix:
            print(row)

    def stringfy(self):
        txt = ''
        for row in self.matrix:
            for col in row:
                try:
                    txt += col
                except Exception:
                    pass
        return txt

    def mixx(self,key):
        while self.matrix[0]:
            pass


    def stringfi(self):
        if type(self.matrix[0][0]) == str:
            return self.stringfy()
        else:
            for row in range(len(self.matrix)):
                for col in range(len(self.matrix[row])):
                    self.matrix[row][col] = self.matrix[row][col].stringfi()

    def mixer(self,key):
        if type(self.matrix[0][0]) == str:
            self.mix(key)
            return self.stringfy()
        else:
            for row in range(len(self.matrix)):
                for col in range(len(self.matrix[row])):
                    self.matrix[row][col] = self.matrix[row][col].mixer(key)



