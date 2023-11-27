from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from gallery.database import get_db
from . import schemas, crud
from gallery.security import ignore_non_admins

router = APIRouter()


@router.post(
    "/breeds/new",
    response_model=schemas.OutputNewBreed,
    dependencies=[Depends(ignore_non_admins)],
)
async def add_breed(
    breed: schemas.NewBreed,
    db: Session = Depends(get_db),
):
    return crud.add_breed(db, breed)


@router.post(
    "/puppies/new",
    response_model=schemas.OutputNewPuppy,
    dependencies=[Depends(ignore_non_admins)],
)
async def add_puppy(
    puppy: schemas.NewPuppy,
    db: Session = Depends(get_db),
):
    tmp = crud.add_puppy(db, puppy)
    return tmp


@router.get(
    "/puppies/{puppy_id}",
    response_model=schemas.OutputPuppyWithBreedStr,
)
def get_puppy(
    puppy_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_puppy(db, puppy_id)
