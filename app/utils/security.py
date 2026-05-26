# import os
from datetime import datetime, timedelta, timezone
from typing import Any, cast

import bcrypt
from app.core.config import settings
from dotenv import load_dotenv
from jose import JWTError, jwt

_ = load_dotenv()

# config
SECRET_KEY = settings.JWT_SECRET_KEY

ALGORITHM = settings.JWT_ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


# hashing password
def hash_password(password: str) -> str:

    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)

    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:

    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


# jwt token
def create_access_token(data: dict[str, Any]) -> str:

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str) -> dict[str, Any]:

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        return cast(dict[str, Any], payload)

    except JWTError:
        raise JWTError("Token tidak valid")
