from ..Enc.enc import  Enc as enc


def get_nearist_2_power(num):
    curr_num = 2
    counter = 0
    while curr_num < num:
        curr_num *= 2
        counter += 1
    return counter

def test_split_and_hash() -> None:
    hash = enc.convert_to_hash("test_test")
    func_result = enc.split_and_hash(hash)
    assert len(func_result) == 2 and type(func_result) == list 

def test_create_list() -> None:
    txt = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent eget nisl quis urna placerat pretium. Proin dignissim erat sapien, vitae ornare odio tempor non. Pellentesque finibus massa a arcu dictum sollicitudin. In interdum massa vitae dolor aliquam elementum. Sed euismod lacus et elit s"""
    key = "test_key_123"

    supposed_size = get_nearist_2_power(len(txt))
    hashed_key = enc.convert_to_hash(key)

    assert len(enc.create_list(hashed_key,len(txt))) == supposed_size

