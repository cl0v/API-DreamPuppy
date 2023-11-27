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
from fastapi.responses import JSONResponse
from fastapi import Request

from gallery.src.feat.gallery.routes import router as gallery_router
from gallery.src.feat.gallery.exceptions import GalleryException

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(gallery_router)


@app.exception_handler(GalleryException)
async def gallery_exception_handler(request: Request, exc: GalleryException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "msg": exc.message,
        },
    )



# app.include_router(items.router)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


##### A PARTIR DAQUI EH SO COISA Q N USO, EXEMPLO DA DOC OFICIAL #####
##### A PARTIR DAQUI EH SO COISA Q N USO, EXEMPLO DA DOC OFICIAL #####
##### A PARTIR DAQUI EH SO COISA Q N USO, EXEMPLO DA DOC OFICIAL #####
##### A PARTIR DAQUI EH SO COISA Q N USO, EXEMPLO DA DOC OFICIAL #####
##### A PARTIR DAQUI EH SO COISA Q N USO, EXEMPLO DA DOC OFICIAL #####
##### A PARTIR DAQUI EH SO COISA Q N USO, EXEMPLO DA DOC OFICIAL #####


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
