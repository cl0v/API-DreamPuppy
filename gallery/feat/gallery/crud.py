from . import schemas, exceptions
from fastapi import status
from sqlalchemy.orm import Session
from gallery.feat.puppy import models as puppy_models
from gallery.feat.puppy.s3_storage import get_url_by_key


LIMIT_AMOUNT = 30
# Ja foi revisado pelos moderadores
REVIEWED_DEFAULT = True
# Está disponível para visualizar na galeria (public_access column)
VISIBLE_DEFAULT = True


def fill_gallery(db: Session, amount: int = 9) -> list[schemas.GallerySchema]:
    if amount > LIMIT_AMOUNT:
        raise exceptions.GalleryException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Too many items",
        )
    q = (
        db.query(
            puppy_models.Media.puppy,
            puppy_models.Media.uuid,
            puppy_models.PuppyModel.uuid,
        )
        .join(
            puppy_models.PuppyModel,
            puppy_models.Media.puppy == puppy_models.PuppyModel.id,
        )
        .filter(
            puppy_models.PuppyModel.reviewed == REVIEWED_DEFAULT,
            puppy_models.PuppyModel.public_access == VISIBLE_DEFAULT,
        )
        .group_by(puppy_models.Media.puppy)
        .limit(amount)
        .all()
    )
    result = [
        {
            "id": id,
            "url": get_url_by_key(puppy_uuid, media_uuid),
        }
        for id, media_uuid, puppy_uuid in q
    ]

    return result
