from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from gallery.schemas import user as schema
from gallery.models import user as model

from fastapi import HTTPException, status


def get_user(db: Session, user_id: int) -> model.User:
    return db.query(model.User).filter(model.User.id == user_id).first()


def create_user(db: Session, user: schema.UserCreate) -> model.User:
    db_user = model.User(cpf=user.cpf, name=user.name)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        # TODO: Verificar se é o CPF mesmo
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="CPF já cadastrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return db_user


# Valida se o user já existe, rejeita o request caso afirmativo.
def validate_user_exists():
    pass


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
