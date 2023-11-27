from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from gallery.database import get_db
from . import schemas, crud

router = APIRouter()


# Garantir que essa rota seja segura
@router.post("/breeds/new", response_model=schemas.OutputBreed)
async def add_breed(breed: schemas.NewBreed, db: Session = Depends(get_db)):
    return crud.add_breed(db, breed)


# Garantir que essa rota seja segura
@router.post("/puppies/new", response_model=schemas.OutputPuppy)
async def add_puppy(puppy: schemas.NewPuppy, db: Session = Depends(get_db)):
    tmp = crud.add_puppy(db, puppy)
    return tmp
