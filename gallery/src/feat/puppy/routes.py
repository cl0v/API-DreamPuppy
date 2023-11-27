from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from gallery.database import get_db
from .schemas import NewPuppySchema, NewBreedSchema, NewBreedOutput
from . import crud

router = APIRouter()


# Garantir que seja seguro essa rota
@router.post("/puppies/new")
def add_puppy(puppy: NewPuppySchema, db: Session = Depends(get_db)):
    return crud.add_puppy(db, puppy)


@router.post("/breeds/new", response_model=NewBreedOutput)
def add_breed(breed: NewBreedSchema, db: Session = Depends(get_db)):
    return crud.add_breed(db, breed)
