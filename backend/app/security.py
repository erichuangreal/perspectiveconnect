import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.config import settings

# Use Argon2 for password hashing (no 72-byte limit like bcrypt)
# Requires argon2-cffi to be installed in the environment.
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    if password is None:
        password = ""
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    if password is None:
        password = ""
    return pwd_context.verify(password, password_hash)

def create_token(user_id: int) -> str:
    exp = datetime.utcnow() + timedelta(days=settings.JWT_EXPIRE_DAYS)
    payload = {"sub": str(user_id), "exp": exp}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

def decode_token(token: str) -> int:
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    return int(payload["sub"])
