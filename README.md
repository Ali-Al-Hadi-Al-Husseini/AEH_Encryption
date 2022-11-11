# AEH Encryption
AEH is a new Encryption algorithm founded by Ali Al Hadi. To Test AEH fork it on [replit](https://replit.com/@Ali-Al-Hadi-Al-Husseini/AEH-encryption#main.py) and uncomment the code


## Usage

```python
from AEH import AE
txt = 'something'
key = 'key'
encrypted = AE.Encrypt(txt, key)
dcrypted = AE.Decrypt(txt, key)
```
## Data streaming
```python
from AEH import AE
sender_object = AE(Key)
txt_1 = sender_object.stream(text_to_be_encoded)
txt_2 = sender_object.stream(another_text_to_be_encoded)

receiver_object = AE(Key)
decoded_txt_1 = sender_object.decrypt_stream(txt_1) ( returns text_to_be_encoded)
decoded_txt_2 = sender_object.decrypt_stream(txt_2) ( returns another_text_to_be_encoded)

```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

need to add modes
