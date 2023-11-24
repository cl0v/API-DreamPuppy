from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from .models import UserCredentials
from datetime import datetime, timedelta
from typing import Annotated, Tuple
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .database import get_db


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
    db.refresh(credentials)

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


def set_user_id_from_jwt(
    db: Session,
    user_id: int,
    token: str = Depends(oauth2_scheme),
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")

    credentials = (
        db.query(UserCredentials)
        .filter(UserCredentials.jwt == token and UserCredentials.email == username)
        .first()
    )

    credentials.user_id = user_id
    db.refresh(credentials)


class JWTVerification:
    def __init__(
        self, db: Session = Depends(get_db), token: str | None = Depends(oauth2_scheme)
    ):
        self.db = db
        self.token = token

    def __call__(self):
        if not self.token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Faça login para continuar",
                headers={"WWW-Authenticate": "Bearer"},
            )
        payload = jwt.decode(self.token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")

        credentials = (
            self.db.query(UserCredentials)
            .filter(
                UserCredentials.jwt == self.token and UserCredentials.email == username
            )
            .first()
        )

        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return credentials.jwt

    def update_user_id(self, user_id: int):
        credentials = (
            self.db.query(UserCredentials)
            .filter(UserCredentials.jwt == self.token)
            .first()
        )
        
        credentials.user_id = user_id

        self.db.commit()
