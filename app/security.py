# from datetime import datetime, timedelta
from typing import Annotated

# from passlib.context import CryptContext
# from pydantic import BaseModel
from fastapi import HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer

# from jose import jwt
# from jose.exceptions import ExpiredSignatureError
# from sqlalchemy.orm import Session
# from sqlalchemy.exc import IntegrityError

# from app.database import get_db
# from app.models import user
from app.env import ADMIN_JWT


# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_DAYS = 30


admin_token = ADMIN_JWT


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"full_name": "Nome de usuário"},
)


def ignore_non_admins(token: Annotated[str, Security(oauth2_scheme)]):
    if token != admin_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autorizado",
        )


# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class TokenData(BaseModel):
#     email: str
#     user_credential_id: int
#     user_id: int


# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password):
#     return pwd_context.hash(password)


# def create_access_token(data: dict) -> str:
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# def authenticate_user_credentials(
#     db: Session,
#     username: str,
#     password: str,
# ) -> Tuple[Token | None, int | None]:
#     hashed_password = get_password_hash(password)
#     credentials = (
#         db.query(user.UserCredentials)
#         .filter(
#             user.UserCredentials.email == username
#             and user.UserCredentials.pwd == hashed_password
#         )
#         .first()
#     )

#     if not credentials:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Email ou senha incorretos",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     if not credentials.user_id:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Usuário não cadastrado",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     credentials.jwt = create_access_token(data={"sub": str(credentials.user_id)})

#     db.commit()
#     db.refresh(credentials)

#     return {
#         "access_token": credentials.jwt,
#         "token_type": "bearer",
#     }, credentials.user_id


# def register_user_credentials(
#     db: Session,
#     username: str,
#     password: str,
# ) -> Token:
#     pass_len = 6
#     if len(password) < pass_len:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"A senha precisa de no mínimo {pass_len} caracteres",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     hashed_password = get_password_hash(password)

#     access_token = create_access_token(data={"sub": ""})

#     credentials = user.UserCredentials(
#         email=username,
#         pwd=hashed_password,
#         jwt=access_token,
#     )

#     try:
#         db.add(credentials)
#         db.commit()
#         db.refresh(credentials)
#     except IntegrityError:
#         raise HTTPException(
#             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             detail="E-mail já registrado",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     return {"access_token": access_token, "token_type": "bearer"}


# def add_user_id_to_credentials(
#     db: Session,
#     token: str,
#     user_id: int,
# ):
#     credentials = (
#         db.query(user.UserCredentials).filter(user.UserCredentials.jwt == token).first()
#     )

#     credentials.user_id = user_id

#     db.commit()


# def validate_jwt(
#     token: Annotated[str, Security(oauth2_scheme)],
#     db: Session = Depends(get_db),
# ):
#     if not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Faça login para continuar",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     except ExpiredSignatureError as err:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Faça login novamente para continuar",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     user_id_str: str = payload.get("sub")

#     if user_id_str == "":
#         user_id = None
#     else:
#         user_id = int(user_id_str)

#     credentials = (
#         db.query(user.UserCredentials)
#         .filter(
#             user.UserCredentials.jwt == token
#             and user.UserCredentials.user_id == user_id
#         )
#         .first()
#     )

#     if not credentials:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Credenciais não encontradas",
#             headers={"WWW-Authenticate": "Bearer"},
#         )


# def user_id_from_token(token: Annotated[str, Security(oauth2_scheme)]) -> int:
#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

#     user_id_str = payload.get("sub")

#     if user_id_str == "":
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Não foi possível encontrar o cadastro de usuário",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     user_id = int(user_id_str)

#     return user_id
