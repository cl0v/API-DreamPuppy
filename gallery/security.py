from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import ExpiredSignatureError
from gallery import models
from datetime import datetime, timedelta
from typing import Annotated, Tuple
from fastapi import Depends, HTTPException, status, Security
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from gallery.database import get_db


from gallery.env import SECRET_KEY


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str
    user_credential_id: int
    user_id: int


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
        db.query(models.UserCredentials)
        .filter(
            models.UserCredentials.email == username
            and models.UserCredentials.pwd == hashed_password
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

    credentials = models.UserCredentials(
        email=username, pwd=hashed_password, jwt=access_token
    )

    try:
        db.add(credentials)
        db.commit()
        db.refresh(credentials)
    except IntegrityError:
        return None, 1

    return {"access_token": access_token, "token_type": "bearer"}, None


class JWTVerification:
    def __init__(
        self,
        token: Annotated[str, Security(oauth2_scheme)],
        db=Annotated[Session, Depends(get_db)],
    ):
        self.db = db
        self.token = token

    def __call__(self) -> str:
        if not self.token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Faça login para continuar",
                headers={"WWW-Authenticate": "Bearer"},
            )
        try:
            payload = jwt.decode(self.token, SECRET_KEY, algorithms=[ALGORITHM])
            print(f"payload {payload}")
        except Exception as err:
            print(err)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Faça login novamente para continuar",
                headers={"WWW-Authenticate": "Bearer"},
            )

        expiration = payload.get("exp")

        # Convert the "exp" claim to a datetime object (assuming it's in Unix timestamp format)
        exp_datetime = datetime.utcfromtimestamp(expiration)

        # Get the current time
        current_time = datetime.utcnow()

        # Compare the "exp" claim with the current time
        if exp_datetime < current_time:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Faça login novamente para continuar",
                headers={"WWW-Authenticate": "Bearer"},
            )

        username: str = payload.get("sub")

        credentials = (
            self.db.query(models.UserCredentials)
            .filter(
                models.UserCredentials.jwt == self.token
                and models.UserCredentials.email == username
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
            self.db.query(models.UserCredentials)
            .filter(models.UserCredentials.jwt == self.token)
            .first()
        )

        credentials.user_id = user_id

        self.db.commit()


def validate_jwt(
    token: Annotated[str, Security(oauth2_scheme)],
    db: Session = Depends(get_db),
):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Faça login para continuar",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Faça login novamente para continuar",
            headers={"WWW-Authenticate": "Bearer"},
        )
   
    username: str = payload.get("sub")

    credentials = (
        db.query(models.UserCredentials)
        .filter(
            models.UserCredentials.jwt == token
            and models.UserCredentials.email == username
        )
        .first()
    )

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
