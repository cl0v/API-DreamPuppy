from .schemas import GallerySchema
from gallery_api_impl.feat.gallery import crud
from gallery_api_impl.database import get_db
from fastapi import APIRouter, Depends, Header
from fastapi_pagination import Page
from typing import Annotated

router = APIRouter()


@router.get("/gallery")
def fill_gallery(
    db=Depends(get_db),
    lat: Annotated[float | None, Header()] = None,
    lon: Annotated[float | None, Header()] = None,
) -> Page[GallerySchema]:
    return crud.fill_gallery(db, lat=lat, lon=lon)


# @router.get("/gallery", response_model=list[GallerySchema])
# Dev gallery (Exibir todos os filhotes que ainda precisam ser aprovados.)
