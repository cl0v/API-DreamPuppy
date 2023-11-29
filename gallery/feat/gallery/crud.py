from . import schemas, exceptions
from fastapi import status
from sqlalchemy.orm import Session, joinedload
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
        db.query(puppy_models.Media.puppy, puppy_models.Media.url)
        .join(
            puppy_models.PuppyModel,
            puppy_models.Media.puppy == puppy_models.PuppyModel.id,
        )
        .filter(
            puppy_models.PuppyModel.reviewed == REVIEWED_DEFAULT,
            puppy_models.PuppyModel.visible == VISIBLE_DEFAULT,
        )
        .group_by(puppy_models.Media.puppy)
        .limit(amount)
        .all()
    )
    result = [{"id": id, "url": img} for id, img in q]

    return result
