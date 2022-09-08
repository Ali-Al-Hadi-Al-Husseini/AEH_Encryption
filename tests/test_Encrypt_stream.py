from ..Enc.AEH import  AE as ae
import unittest


class TestStream(unittest.TestCase):

    def setUp(self) -> None:
        keys = ["asdasdsa",'1234567','Lt_@&&786mti']
        self.ae_objects = [ae(key) for key in keys]
        self.test_case = [
                    "soiibsudyfsdioufbdsoifbsdofsdouyf",
                    "dsaduysan a nuysaun ysiuaysiuay asiudyasiudyasiuyd da",
                    "lorem ipsum where here and where are you there and he is here nad he is their and where are yopu"
        ]


    def test_Stream(self):
        for obj in self.ae_objects:
            for txt in self.test_case:
                temp = obj.Stream(txt)
                self.assertNotEqual(txt,temp)

    def test_decrypt_stream(self):
        for obj in self.ae_objects:
            decrypt_obj = ae(obj.un_hashed)
            for txt in self.test_case:
                temp = obj.Stream(txt)
                result = decrypt_obj.Decrypt_Stream(temp)
                self.assertEqual(result,txt)
                
    



