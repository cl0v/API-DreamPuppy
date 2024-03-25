from sqlalchemy.orm import Session
from . import schemas, models, exceptions
from gallery_api_impl.feat.puppy.models import PuppyModel
from gallery_api_impl.feat.puppy.schemas import OutPuppy
from sqlalchemy.exc import IntegrityError
from fastapi import status
from psycopg2.errors import UniqueViolation
from gallery_api_impl.constants.strings import (
    DUPLICATED_PHONE_ERROR,
    EMPTY_PHONE_ERROR,
    DUPLICATED_INSTAGRAM_ERROR,
    DUPLICATED_KENNEL_ERROR,
)


def add_kennel(db: Session, kennel: schemas.CreateKennel) -> models.KennelModel:
    model = models.KennelModel(**kennel.model_dump())

    if kennel.phone == "":
        raise exceptions.KennelException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=EMPTY_PHONE_ERROR,
        )

    duplicatePhone = (
        db.query(models.KennelModel)
        .filter(models.KennelModel.phone == kennel.phone)
        .first()
    )

    duplicateInstagram = kennel.instagram != "" and (
        db.query(models.KennelModel)
        .filter(models.KennelModel.instagram == kennel.instagram)
        .first()
    )

    if duplicatePhone:
        raise exceptions.KennelException(
            status_code=status.HTTP_409_CONFLICT,
            message=DUPLICATED_PHONE_ERROR,
        )

    if duplicateInstagram and kennel.instagram != "":
        raise exceptions.KennelException(
            status_code=status.HTTP_409_CONFLICT,
            message=DUPLICATED_INSTAGRAM_ERROR,
        )

    try:
        db.add(model)
        db.flush()
        db.commit()
    except IntegrityError as err:
        db.rollback()
        if type(err.orig) is UniqueViolation:
            raise exceptions.KennelException(
                status_code=status.HTTP_409_CONFLICT,
                message=DUPLICATED_KENNEL_ERROR,
            )
        raise err

    db.refresh(model)
    return model


def get_kennel(db: Session, kennel_id: int) -> models.KennelModel:
    model = (
        db.query(models.KennelModel).filter(models.KennelModel.id == kennel_id).first()
    )
    if not model:
        raise exceptions.KennelException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Canil não existe.",
        )

    return model


def list_my_puppies(db: Session, kennel_id: int) -> list[OutPuppy]:
    q = (
        db.query(PuppyModel)
        .filter(PuppyModel.kennel == kennel_id)
        .all()
    )

    return q
