from sqlalchemy.orm import Session
from . import schemas, models, exceptions
from sqlalchemy.exc import IntegrityError
from fastapi import status
from psycopg2.errors import UniqueViolation


def add_kennel(db: Session, kennel: schemas.CreateKennel) -> models.KennelModel:
    model = models.KennelModel(**kennel.model_dump())
    
    # Primeiro devo checar se os valores primary key ja foram usados, retornar erro antes de tentar adicionar.
    
    duplicatePhone = (
        db.query(models.KennelModel).filter(models.KennelModel.phone == kennel.phone).first()
    )
    duplicateInstagram = (
        db.query(models.KennelModel).filter(models.KennelModel.instagram == kennel.instagram).first()
    )
    
    if duplicatePhone:
         raise exceptions.KennelException(
                status_code=status.HTTP_409_CONFLICT,
                message="Telefone já cadastrado, tente outro.",
            )
    if duplicateInstagram:
         raise exceptions.KennelException(
                status_code=status.HTTP_409_CONFLICT,
                message="Instagram já cadastrado, tente outro.",
            )
    
    try:
        db.add(model)
        db.commit()
        db.refresh(model)
    except IntegrityError as err:
        print(err.orig)
        if(type(err.orig) is UniqueViolation):
            
        # duplicate_param_name = err.args[0].split("kennels.")[1]
            raise exceptions.KennelException(
                status_code=status.HTTP_409_CONFLICT,
                message="Canil já está cadastrado, tente outro.",
            )
    return model


def get_kennel(db: Session, kennel_id: int) -> models.KennelModel:
    model = (
        db.query(models.KennelModel).filter(models.KennelModel.id == kennel_id).first()
    )
    if not model:
        raise exceptions.KennelException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Canil não encontrado.",
        )

    print(model)
    return model


def relate_to_kennel_n_puppies(db: Session, kennel_id: int, puppy_id: int):
    model = models.KennelsNPuppies(kennel_id=kennel_id, puppy_id=puppy_id)
    db.add(model)
    db.commit()
    db.refresh(model)


def list_my_puppies_ids(db: Session, kennel_id: int) -> list[int]:
    q = (
        db.query(models.KennelsNPuppies)
        .filter(models.KennelsNPuppies.kennel_id == kennel_id)
        .all()
    )

    tmp = []

    for r in q:
        tmp.append(r.puppy_id)

    return tmp
