from datetime import datetime, timedelta

from jose import jwt

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_EXPIRE_MIN = 15
REFRESH_EXPIRE_DAYS = 7


def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + expires_delta
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(user_id: str):
    return create_token({"sub": user_id}, timedelta(minutes=ACCESS_EXPIRE_MIN))


def create_refresh_token(user_id: str):
    return create_token({"sub": user_id}, timedelta(days=REFRESH_EXPIRE_DAYS))


def decode_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload["sub"]

