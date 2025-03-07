from datetime import timedelta, datetime

import jwt
import bcrypt
from core.settings import settings


# Функция, которая создает jwt токен
def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.now()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=algorithm,
    )
    return encoded

# Функция, которая декодит jwt токен
def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(
        token,
        key=public_key,
        algorithms=[algorithm],
    )
    return decoded

# Функции для шифрования и для проверки

def hash_password(
        password: str,

) -> bytes:
    salt = bcrypt.gensalt()
    password_bytes: bytes = password.encode()
    return bcrypt.hashpw(password_bytes, salt)

def validate_password(
        password: str,
        hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
