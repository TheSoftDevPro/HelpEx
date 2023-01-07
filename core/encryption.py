from cryptography.fernet import Fernet
from HELPEX.keyconfig import ENCRYPTION_KEY

def raw_to_encrypted(raw_id):
    fernet = Fernet(key = ENCRYPTION_KEY)
    encrypted = fernet.encrypt(raw_id.encode())
    return encrypted

def encrypted_to_raw(encrypted):
    fernet = Fernet(key = ENCRYPTION_KEY)
    raw = fernet.decrypt(encrypted).decode()
    return raw
    
# print(Fernet.generate_key())
