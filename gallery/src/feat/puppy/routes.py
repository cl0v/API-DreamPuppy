from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from gallery.database import get_db
from .schemas import NewPuppySchema
from . import crud

router = APIRouter()


@router.post("/puppies/new")
# Garantir que seja seguro essa rota
def add_puppy(puppy: NewPuppySchema, db: Session = Depends(get_db)):
    return crud.add_puppy(db, puppy)
