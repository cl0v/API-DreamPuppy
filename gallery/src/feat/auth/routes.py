from fastapi.datastructures import URL
from fastapi.responses import RedirectResponse
import uvicorn

from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status, Body, Header
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from gallery.database import get_db, engine, Base
from gallery.security import (
    Token,
    oauth2_scheme,
    validate_jwt,
    user_id_from_token,
    add_user_id_to_credentials,
    register_user_credentials,
    authenticate_user_credentials,
)



# import gallery.models.user as user_model
import gallery.schemas.user as user_schema
import gallery.cruds.user as user_crud
from gallery.cruds.user import validate_user_exists

from main import app

@app.post("/auth/register", response_model=Token)
async def register_for_credentials(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    credentials = register_user_credentials(db, form_data.username, form_data.password)
    return credentials


@app.post(
    "/users/new",
    dependencies=[Depends(validate_jwt), Depends(validate_user_exists)],
    response_model=user_schema.UserWithToken,
)
def new_user(
    user: Annotated[user_schema.UserCreate, Body()],
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    new_user = user_crud.create_user(db, user)
    # TODO: Verificar possiveis problemas de fluxo (User já cadastrado)
    add_user_id_to_credentials(db, token, new_user.id)
    print(new_user)


    return new_user


@app.post("/auth/login", response_model=user_schema.UserWithToken)
async def login_for_credentials(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    token, user_id = authenticate_user_credentials(
        db, form_data.username, form_data.password
    )

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = user_crud.get_user(db, user_id)

    return user_schema.UserWithToken(**token, id=user.id, name=user.name)

