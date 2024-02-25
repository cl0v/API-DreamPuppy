from .schemas import GallerySchema
from app.feat.gallery import crud
from app.database import get_db
from fastapi import APIRouter, Depends
from fastapi_pagination import Page
router = APIRouter()


@router.get("/gallery")
def fill_gallery(amount: int = 9, db=Depends(get_db)) -> Page[GallerySchema]:
    return (crud.fill_gallery(db, amount))


# @router.get("/gallery", response_model=list[GallerySchema])
# Dev gallery (Exibir todos os filhotes que ainda precisam ser aprovados.)
