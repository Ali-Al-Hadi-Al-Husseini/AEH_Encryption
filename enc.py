from hashlib import sha256

def create_list(key,size):
    x = int(size/64) + 1
    this_list= [sha256(key.encode()).hexdigest()]
    this_list.extend(split_hash(this_list[0]))

    for i in range(x-1):
        x = ((len(this_list)+1)//2 ) -1
        print(x)
        for i in this_list[x:]:
            this_list.extend(split_hash(i)) 
            

    return this_list

def split_hash(key):
    x = int(len(key) /2)
    return list([sha256(key[x:].encode()).hexdigest(),sha256(key[:x].encode()).hexdigest()])


    



