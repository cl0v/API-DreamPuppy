from fastapi import APIRouter, Depends, File, Form, UploadFile

# from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from gallery.database import get_db
from . import schemas, crud, exceptions, types
from gallery.security import ignore_non_admins
from fastapi import status
from gallery.feat.puppy import crud as puppy_crud
from gallery.feat.puppy.schemas import NewPuppy, OutputNewPuppy
from typing import Annotated

router = APIRouter()


@router.post(
    "/kennels/new",
    response_model=schemas.OutputKennel,
    dependencies=[Depends(ignore_non_admins)],
)
async def add_kennel(kennel: schemas.CreateKennel, db: Session = Depends(get_db)):
    return crud.add_kennel(db, kennel)


@router.get(
    "/kennels/{kennel_id}",
    response_model=schemas.OutputKennelWithCitySchema,
)
async def get_kennel(kennel_id: int, db: Session = Depends(get_db)):
    return crud.get_kennel(db, kennel_id)


@router.post(
    "/kennels/{kennel_id}/puppies/new",
    # response_model=OutputNewPuppy,
    dependencies=[Depends(ignore_non_admins)],
)
def add_puppy(
    puppy: Annotated[types.PuppyRequestForm, Depends()],
    images: Annotated[UploadFile, File()],
    kennel_id: int,
    db: Session = Depends(get_db),
):
    
    print(images)
    return {
        "content_type": images,
        "kennel_id": kennel_id,
        "puppy": puppy.age,
    }

    n_puppy = puppy_crud.add_puppy(db, puppy)
    crud.relate_to_kennel_n_puppies(db, kennel_id, n_puppy.id)

    return n_puppy


@router.get(
    "/kennels/{kennel_id}/puppies/",
    response_model=list[OutputNewPuppy],
    dependencies=[Depends(ignore_non_admins)],
)
def list_puppies_from_kennel(
    kennel_id: int,
    db: Session = Depends(get_db),
):
    ids = crud.list_my_puppies_ids(db, kennel_id)
    tmp = puppy_crud.list_puppies_form_id(db, ids)
    return tmp
