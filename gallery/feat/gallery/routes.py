from .schemas import GallerySchema
from gallery.feat.gallery import crud
from gallery.database import get_db
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/gallery/", response_model=list[GallerySchema])
def fill_gallery(amount: int = 9, db=Depends(get_db)):
    return crud.fill_gallery(db, amount)


# @router.get("/gallery", response_model=list[GallerySchema])
# Dev gallery (Exibir todos os filhotes que ainda precisam ser aprovados.)
