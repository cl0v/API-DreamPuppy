from sqlalchemy.orm import Session
from gallery.schemas import puppy as schema
from gallery.models import puppy as model

def add_puppy(db: Session, puppy: schema.PuppyBase) -> model.Puppy:
    db_puppy = model.Puppy(**puppy.dict())
    db.add(db_puppy)
    db.commit()
    db.refresh(db_puppy)
    return db_puppy