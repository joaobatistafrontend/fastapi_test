from passlib.context import CryptContext
brcrypt_context = CryptContext(schemes=["argon2"], deprecated="auto")
