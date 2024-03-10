from app.security import ignore_non_admins
from .schemas import GallerySchema
from app.feat.gallery import crud
from app.database import get_db
from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/gallery")
def fill_gallery(db=Depends(get_db)) -> Page[GallerySchema]:
    return crud.fill_gallery(db)


@router.put(
    "/gallery/fix",
    response_model=list[str],
    description="This method will remove and alert about all puppies showing on gallery that doesn't have any public images on details page.",
    dependencies=[Depends(ignore_non_admins)],
)
def fix_showing_puppy_on_gallery(
    db: Session = Depends(get_db),
):
    id_list = crud.hide_puppies_without_public_image(db)
    return id_list


# @router.get("/gallery", response_model=list[GallerySchema])
# Dev gallery (Exibir todos os filhotes que ainda precisam ser aprovados.)
