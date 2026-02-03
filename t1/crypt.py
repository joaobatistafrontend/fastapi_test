from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
brcrypt_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login-form")
