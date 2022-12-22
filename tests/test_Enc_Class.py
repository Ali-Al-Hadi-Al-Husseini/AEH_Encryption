from enc import  *
from testing_utils import get_nearist_2_power,get_nearist_2_power_until_64
from unittest import TestCase




class TestEncClass(TestCase):
    
    def test_create_list(self) -> None:
        test_cases = [
                    ("""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent eget nisl quis urna placerat pretium. Proin dignissim erat sapien, vitae ornare odio tempor non. Pellentesque finibus massa a arcu dictum sollicitudin. In interdum massa vitae dolor aliquam elementum. Sed euismod lacus et elit s""","test_key_123"),
                    ("holala go me 124",'test123'),
                    ("hola gola me 124" * 7,'test123'),
                    ("Don't be the same be better !  quote of the day "* 7,'quote124'),

        ]
        for txt,key in test_cases:
            supposed_size =(get_nearist_2_power_until_64(len(txt))) 
            hashed_key = Keys.convert_to_hash(key)
            size = len(Keys.create_list(hashed_key,len(txt)))

            self.assertEqual(size,supposed_size)


    def test_split_and_hash(self) -> None:
        hash = Keys.convert_to_hash("test_test")
        func_result = Keys.split_and_hash(hash)
        self.assertTrue(len(func_result) == 2 and type(func_result) == list) 

    def test_create_hash_list(self):
        test_cases = [
            ('123_@78fam',200),
            ('1c345vvas',1000),
            ("hola_@124&*?1a",20)

        ]

        for key,size in test_cases:
            hash_list,_ = Keys.create_hash_list(key,size)
            has_right_size = len(hash_list) == 2 ** (get_nearist_2_power(size * 5))
            self.assertTrue(has_right_size)

    def test_generate_keylist(self):
        test_cases = [
            ('123_@78fam',200,'sasd'),
            ('1c345vvas',1000,'kk'),
            ("hola_@124&*?1a",20,'NONE'),
            ('123_@78fam',200,'NONE'),
            ("hola_@124&*?1a",10000,'NONE'),
            ('123_@78fam',9000,'NONE'),
            ('1c345vvas',6600,'NONE'),
        ]

        for key,size,case in test_cases:
            keys_list = Keys.generate_keylist(size * 5,key,1,case)
            self.assertTrue(len(keys_list) > size)

            for num in keys_list:
                self.assertTrue(type(num) == int)

    def test_generate_nums(self):
        test_cases_success = [
            ([1,2,3,4,5],"NONE"),
            ([1,2,3,4,5],"as"),
            ([10,22,99,30,9],"aS"),
            ([10,22,99,30,9],"NONE"),
            ([11,22,33,44,55],'NONE'),
            ([11,22,33,44,55],'as'),
            ([0,0,0,0,0],'NONE'),
            ([0,0,0,0,0],'AS'),
            ([20,0,0,1,0],"b")

        ]
        test_cases_fail = [
                [1],
                [],
                [1,3,3]
        ]

        for List,case in test_cases_success:
            self.assertTrue(type(Keys.generate_nums(List,case)),int)

        for List in test_cases_fail:
            self.assertRaises(ValueError,lambda: Keys.generate_nums(List))

    def test_generate_shuffle_list(self):
        test_cases_success = [
            ('123_@78fam',200),
            ('1c345vvas',1000),
            ("hola_@124&*?1a",20),
            ('123_@78fam',200),
            ('1c345vvas',1000),
        ]


        for key,len_txt in test_cases_success:
            shuffle_list = Shuffle.generate_shuffle_list(len_txt,len_txt,key)
            has_the_right_length = len(shuffle_list) == len_txt
            has_the_right_numbers = True

            for num in shuffle_list:
                self.assertFalse(num < 0 or num >= len_txt)
            
            self.assertTrue(has_the_right_numbers and has_the_right_length)

    def test_shuffle(self):
        test_cases = [
                (" aslfkasjl sadsfasf fsafasf as,skmp op ",'124asda'),
                ("Lorem opsium man how are you there and not here a\but are you not anywhere",'@12/13casd'),
                ('12345r',"12"),
                ('','')
        ]

        for txt, key in test_cases:
            shuffled  = Shuffle.shuffle(txt,Keys.convert_to_hash(key))

            self.assertTrue(len(txt) == len(shuffled))
            self.assertTrue(txt != shuffled or txt == '')

            txt_set = set(list(txt))

            for Char in shuffled:
                self.assertTrue(Char in txt_set)

    def test_un_shuffle(self):
        test_cases = [
                (" aslfkasjl sadsfasf fsafasf as,skmp op ",'124asda'),
                ("Lorem opsium man how are you there and not here a\but are you not anywhere",'@12/13casd'),
                ('12345r',"12"),
                ('','')
        ]

        for txt,key in test_cases:
            Hash = Keys.convert_to_hash(key)
            shuffled = Shuffle.shuffle(txt,Hash)
            
            self.assertEqual(txt, Shuffle.un_shuffle(shuffled,Hash))
        

