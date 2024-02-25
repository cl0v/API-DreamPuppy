from . import schemas, exceptions
from fastapi import status
from sqlalchemy.orm import Session
from app.feat.puppy import models as puppy_models
from app.feat.puppy.image_storage import get_gallery_image_url



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
    # select puppy,uuid from medias where puppy in (SELECT id FROM puppies WHERE puppies.reviewed=True AND puppies.public_access=True);
    
    # SELECT id FROM puppies WHERE puppies.reviewed=True AND puppies.public_access=True
    
    q = (
        db.query(
            puppy_models.Media.puppy,
            puppy_models.Media.uuid,
            # puppy_models.PuppyModel.uuid,
        )
        .join(
            puppy_models.PuppyModel,
            puppy_models.Media.puppy == puppy_models.PuppyModel.id,
        )
        .filter(
            puppy_models.PuppyModel.reviewed == REVIEWED_DEFAULT,
            puppy_models.PuppyModel.public_access == VISIBLE_DEFAULT,
        )
        .group_by(
            puppy_models.Media.puppy,
            puppy_models.Media.uuid,
            puppy_models.PuppyModel.uuid,
        ).distinct(puppy_models.Media.puppy)
        .limit(amount)
        .all()
    )

    result = [
        {
            "id": id,
            "url": get_gallery_image_url(media_uuid),
        }
        for id, media_uuid in q
    ]

    return result
