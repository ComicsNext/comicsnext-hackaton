from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings
import bcrypt

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES



def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed)



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    expire = datetime.now() + (expires_delta or timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    ))

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def _pre_hash(password: str) -> str:
#     """
#     Pre-hash SHA256 para evitar límite de 72 bytes de bcrypt
#     """
#     return sha256(password.encode("utf-8")).hexdigest()


# def hash_password(password: str) -> str:
#     return pwd_context.hash(_pre_hash(password))


# def verify_password(plain: str, hashed: str) -> bool:
#     return pwd_context.verify(_pre_hash(plain), hashed)

