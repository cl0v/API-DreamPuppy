from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from . import schemas, crud, exceptions
from app.security import ignore_non_admins
from fastapi import status
from app.feat.puppy import crud as puppy_crud
from app.feat.puppy.schemas import (
    PuppyRequestForm,
    OutPuppy,
    OutputPuppyWithBreedStr,
)
from typing import Annotated

router = APIRouter()


# App Gallery:
@router.get(
    "/kennels/{kennel_id}",
    response_model=schemas.OutputKennel,
)
async def get_kennel(kennel_id: int, db: Session = Depends(get_db)):
    return crud.get_kennel(db, kennel_id)


# App Kennel
@router.post(
    "/kennels/{kennel_id}/puppies/new",
    response_model=schemas.OutputAddPuppy,
    dependencies=[Depends(ignore_non_admins)],
)
def add_puppy(
    kennel_id: int,
    puppy: Annotated[PuppyRequestForm, Depends()],
    db: Session = Depends(get_db),
    **images: Annotated[list[UploadFile], File()],
):
    n_puppy = puppy_crud.add_puppy(db, images=images, schema=puppy)

    crud.relate_to_kennel_n_puppies(db, kennel_id=kennel_id, puppy_id=n_puppy.id)

    return {"id": n_puppy.id, "message": "OK"}


@router.get(
    "/kennels/{kennel_id}/puppies/",
    response_model=list[OutPuppy],
    dependencies=[Depends(ignore_non_admins)],
)
def list_puppies_from_kennel(
    kennel_id: int,
    db: Session = Depends(get_db),
):
    ids = crud.list_my_puppies_ids(db, kennel_id)
    tmp = puppy_crud.list_puppies(db, ids)
    return tmp


# App Dashboard:
@router.post(
    "/kennels/new",
    response_model=schemas.OutputKennel,
    dependencies=[Depends(ignore_non_admins)],
)
async def add_kennel(kennel: schemas.CreateKennel, db: Session = Depends(get_db)):
    return crud.add_kennel(db, kennel)
