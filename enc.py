from hashlib import sha256


    
class Enc:

    # creater a string that is as the size of the file
    @classmethod
    def create_list(cls,Key,size):
        if size <= 64:
            new_key = []
            new_key.append(Key)
            return new_key

        else:
            new_keys = []
            new_list = cls.create_new_list( cls.create_list( Key,(size * 5) // 2))
            new_keys.extend( new_list)
            return new_keys

    #this method take one parameter (hash as a string) and then returns the hash of the half of the key
    @classmethod
    def split_and_hash(cls,key):
        half_key = int(len(key) /2) + 1
        return list((sha256(key[half_key:].encode()).hexdigest(),sha256(key[:half_key].encode()).hexdigest()))

    @classmethod
    def create_new_list(cls,keys):
        new_keys = []
        for key in keys:
            new_keys.extend( cls.split_and_hash(key))

        return new_keys

    #write the last keys the keys.txt file
    @classmethod
    def  create_file(cls,key,size):
        keys_list = cls.create_list(key,size)
        with open('keys.txt', 'w') as temp:
            for key in keys_list:
                temp.write(key)


