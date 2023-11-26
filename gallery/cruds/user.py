from sqlalchemy.orm import Session

from gallery.schemas import user as schema
from gallery.models import user as model

def get_user(db: Session, user_id: int) -> model.User:
   
    return db.query(model.User).filter(model.User.id == user_id).first()


def create_user(db: Session, user: schema.UserCreate) -> model.User:
    db_user = user.User(cpf=user.cpf, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
