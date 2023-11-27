from sqlalchemy.orm import Session
from .schemas import PuppySchema, NewPuppySchema
from .models import PuppyModel


def add_puppy(db: Session, puppy: NewPuppySchema) -> PuppyModel:
    db_puppy = PuppyModel(**puppy.model_dump())
    db.add(db_puppy)
    db.commit()
    db.refresh(db_puppy)
    return db_puppy


def get_puppy(db: Session, puppy_id: int) -> PuppyModel:
    raise Exception("Unimplemented")
