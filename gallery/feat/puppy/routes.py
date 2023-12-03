from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from gallery.database import get_db
from . import schemas, crud
from gallery.security import ignore_non_admins

router = APIRouter()


# App Gallery:
@router.get(
    "/puppies/{puppy_id}",
    response_model=schemas.OutputPuppyWithBreedStr,
)
def get_puppy(
    puppy_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_puppy(db, puppy_id)


# App Gallery:
@router.get(
    "/puppies/{puppy_id}/kennel",
    response_model=int,
)
def get_puppy(
    puppy_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_kennel_id_from_puppy_id(db, puppy_id)


# App Dashboard:
@router.post(
    "/breeds/new",
    response_model=schemas.OutputNewBreed,
    dependencies=[Depends(ignore_non_admins)],
)
async def add_breed(breed: schemas.NewBreed, db: Session = Depends(get_db)):
    return crud.add_breed(db, breed)


@router.get(
    "/breeds/list",
    response_model=list[schemas.OutputNewBreed],
)
def list_breeds(db: Session = Depends(get_db)):
    return crud.list_breeds(db)


@router.put(
    "/puppies/{puppy_id}/show",
    dependencies=[Depends(ignore_non_admins)],
)
def show_on_gallery(
    puppy_id: int,
    db: Session = Depends(get_db),
):
    pid = crud.show_on_gallery(db, puppy_id)
    return {"id": pid, "message": "OK"}


@router.put(
    "/puppies/{puppy_id}/hide",
    dependencies=[Depends(ignore_non_admins)],
)
def hide_from_gallery(
    puppy_id: int,
    db: Session = Depends(get_db),
):
    pid = crud.hide_from_gallery(db, puppy_id)
    return {"id": pid, "message": "OK"}
