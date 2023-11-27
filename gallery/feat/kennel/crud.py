from sqlalchemy.orm import Session
from . import schemas, models, exceptions
from sqlalchemy.exc import IntegrityError
from fastapi import status


def add_kennel(db: Session, kennel: schemas.CreateKennel) -> models.KennelModel:
    db_kennel = models.KennelModel(**kennel.model_dump())
    try:
        db.add(db_kennel)
        db.commit()
        db.refresh(db_kennel)
    except IntegrityError as err:
        duplicate_param_name = err.args[0].split("kennels.")[1]
        raise exceptions.KennelException(
            status_code=status.HTTP_409_CONFLICT,
            message=f"O {duplicate_param_name} já está cadastrado, tente outro.",
        )
    return db_kennel
