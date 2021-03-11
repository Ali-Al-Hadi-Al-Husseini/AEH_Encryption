# Encryption
This a new way to enctypt files 

```bash
pip install AEH
pip3 install AEH
```

## Usage

```python
from encrypt import AEH
txt = 'something'
key = 'key'
encrypted = AEH.Encrypt(txt, key)
dcrypted = AEH.Decrypt(txt, key)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
