# AEH Encryption
AEH is a new Encryption algorithm founded by Ali Al Hadi. To Test AEH fork it on [replit](https://replit.com/@Ali-Al-Hadi-Al-Husseini/AEH-encryption#main.py) and uncomment the code


## Usage
## stream encryption
```python
from AEH import AE
txt = 'something'
key = 'key'
encrypted = AE.Encrypt(txt, key) # (returns encoded text)
dcrypted = AE.Decrypt(encrypted, key) # (return orginal text after being decoded)
```
## Data streaming
### Used to send data over internert 
```python
from AEH import AE
sender_object = AE(Key)
txt_1 = sender_object.stream(text_to_be_encoded)
txt_2 = sender_object.stream(another_text_to_be_encoded)

receiver_object = AE(Key)
decoded_txt_1 = sender_object.decrypt_stream(txt_1) ( returns text_to_be_encoded)
decoded_txt_2 = sender_object.decrypt_stream(txt_2) ( returns another_text_to_be_encoded)

```
## Block Encryption 
### encrypts data  as a 64 char (256 bit) block
```python
from AEH import AE
sender_object = AE(Key)
txt = 'li la _ 1234' * 7 
key = "123456"

encoded  = AE.Block_Encryption(txt, key )  #  returns encoded text 
decoded = AE.Block_Decryption(encoded,key) # returns decoded text 

```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

need to add modes
