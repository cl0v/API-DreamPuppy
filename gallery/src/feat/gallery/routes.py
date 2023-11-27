from .schemas import GallerySchema
from . import crud

from fastapi import APIRouter

router = APIRouter()


@router.get("/gallery", response_model=list[GallerySchema])
def fill_gallery(amount: int = 9):
    return crud.get_puppies_cover_list(amount)
