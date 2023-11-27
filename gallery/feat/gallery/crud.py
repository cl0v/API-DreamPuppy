from . import schemas, exceptions
from fastapi import status
from sqlalchemy.orm import Session
from gallery.feat.puppy import models as puppy_models


LIMIT_AMOUNT = 30
# Ja foi revisado pelos moderadores
REVIEWED_DEFAULT = True
# Está disponível para visualizar na galeria
VISIBLE_DEFAULT = True


def fill_gallery(db: Session, amount: int = 9) -> list[schemas.GallerySchema]:
    if amount > LIMIT_AMOUNT:
        raise exceptions.GalleryException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Too many items",
        )
    q = (
        db.query(puppy_models.PuppyModel)
        .filter(
            puppy_models.PuppyModel.reviewed == REVIEWED_DEFAULT,
            puppy_models.PuppyModel.visible == VISIBLE_DEFAULT,
        )
        .limit(amount)
        .all()
    )

    return q
