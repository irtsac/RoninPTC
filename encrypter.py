import base64
from cryptography.fernet import Fernet


def encrypt(key, source):

    fernet = Fernet(key)
    encMessage = fernet.encrypt(source.encode())
    return encMessage

def decrypt(key, source):

    fernet = Fernet(key)
    decMessage = fernet.decrypt(source).decode()
    return decMessage
key = Fernet.generate_key()
print(key)
sss = encrypt(key, 'caccola')
print(sss)
scs = decrypt(key, sss)
print(scs)
