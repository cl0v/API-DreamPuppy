from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from .models import UserCredentials
from datetime import datetime, timedelta
from typing import Annotated, Tuple
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from .env import SECRET_KEY


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str
    user_credential_id: int
    user_id: int


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user_credentials(
    db: Session,
    username: str,
    password: str,
) -> Token | None:
    hashed_password = get_password_hash(password)
    credentials = (
        db.query(UserCredentials)
        .filter(
            UserCredentials.email == username and UserCredentials.pwd == hashed_password
        )
        .first()
    )

    if not credentials:
        return None

    credentials.jwt = create_access_token(data={"sub": username})

    db.commit()

    return {"access_token": credentials.jwt, "token_type": "bearer"}


def register_user_credentials(
    db: Session,
    username: str,
    password: str,
) -> Tuple[Token | None, int | None]:
    hashed_password = get_password_hash(password)

    access_token = create_access_token(data={"sub": username})

    credentials = UserCredentials(email=username, pwd=hashed_password, jwt=access_token)

    try:
        db.add(credentials)
        db.commit()
        db.refresh(credentials)
    except IntegrityError:
        return None, 1

    return {"access_token": access_token, "token_type": "bearer"}, None
