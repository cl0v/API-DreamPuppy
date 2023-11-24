from fastapi.datastructures import URL
from fastapi.responses import RedirectResponse
import uvicorn

from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status, Body, Header
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from gallery.database import get_db, engine
from gallery.security import (
    Token,
    oauth2_scheme,
    validate_jwt,
    add_user_id_to_credentials,
    register_user_credentials,
    authenticate_user_credentials,
)

from gallery import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Usar middleware para log de falhas de sistema.


@app.post("/auth/register", response_model=Token)
async def register_for_credentials(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    return register_user_credentials(db, form_data.username, form_data.password)


@app.post(
    "/users/new",
    dependencies=[Depends(validate_jwt)],
    response_model=schemas.User,
)
def create_user(
    user: Annotated[schemas.UserCreate, Body()],
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    new_user = crud.create_user(db, user)
    print(new_user)
    add_user_id_to_credentials(db, token, new_user.id)

    return new_user


@app.post("/auth/login", response_model=schemas.UserWithToken)
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

    user = crud.get_user(db, user_id=user_id)

    return schemas.UserWithToken(**token, id=user.id, name=user.name)


##### A PARTIR DAQUI EH SO COISA Q N USO, EXEMPLO DA DOC OFICIAL #####
##### A PARTIR DAQUI EH SO COISA Q N USO, EXEMPLO DA DOC OFICIAL #####
##### A PARTIR DAQUI EH SO COISA Q N USO, EXEMPLO DA DOC OFICIAL #####
##### A PARTIR DAQUI EH SO COISA Q N USO, EXEMPLO DA DOC OFICIAL #####
##### A PARTIR DAQUI EH SO COISA Q N USO, EXEMPLO DA DOC OFICIAL #####
##### A PARTIR DAQUI EH SO COISA Q N USO, EXEMPLO DA DOC OFICIAL #####


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
