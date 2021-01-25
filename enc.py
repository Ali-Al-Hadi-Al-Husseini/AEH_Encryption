from hashlib import sha256


    
class enc:
    @classmethod
    def create_list(self,key,size):
        x = int(size/64) + 1
        this_list= [sha256(key.encode()).hexdigest()]
        this_list.extend(self.split_hash(this_list[0]))
        srt_k = ''

        for i in range(x-1):
            y = ((len(this_list)+1)//2 ) -1
            for i in this_list[y:]:
                this_list.extend(self.split_hash(i)) 
        for i in this_list:
            srt_k += i

        return str_k
    @classmethod
    def split_hash(self,key):
        x = int(len(key) /2)
        return list([sha256(key[x:].encode()).hexdigest(),sha256(key[:x].encode()).hexdigest()])
    
    

    



