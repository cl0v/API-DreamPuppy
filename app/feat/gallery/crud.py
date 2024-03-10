from . import schemas#, exceptions
# from fastapi import status
from sqlalchemy.orm import Session
from app.feat.puppy import models as puppy_models
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page

LIMIT_AMOUNT = 30
# Ja foi revisado pelos moderadores
REVIEWED_DEFAULT = True
# Está disponível para visualizar na galeria (public_access column)
VISIBLE_DEFAULT = True


def fill_gallery(db: Session) -> Page[schemas.GallerySchema]:
    # TODO: Adicionar limitador de itens
    # if amount > LIMIT_AMOUNT:
    #     raise exceptions.GalleryException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         message="Too many items",
    #     )
    # select puppy,uuid from medias where puppy in (SELECT id FROM puppies WHERE puppies.reviewed=True AND puppies.public_access=True);

    # SELECT id FROM puppies WHERE puppies.reviewed=True AND puppies.public_access=True

    q = (
        db.query(
            puppy_models.PuppyModel.id,
            puppy_models.PuppyModel.cover_url,
            # puppy_models.PuppyModel.uuid,
        )
        .filter(
            puppy_models.PuppyModel.reviewed == REVIEWED_DEFAULT,
            puppy_models.PuppyModel.public_access == VISIBLE_DEFAULT,
            puppy_models.PuppyModel.cover_url.is_not(None)
        )
        .group_by(
            puppy_models.PuppyModel.id,
            puppy_models.PuppyModel.cover_url,
        )
        .order_by(puppy_models.PuppyModel.id.desc())
        # .limit(3)
        # .all()
    )
    
    
    val = paginate(
        db,
        q,
        transformer=lambda q: [
            {
                "id": id,
                "url": cover_url
            }
            for id, cover_url in q
        ],
    )

    return val



def hide_puppies_without_public_image(db: Session) -> list[str]:
    #TODO: Implement
    # Filhotes que estao sendo exibidos porém public_url das medias estão sem nenhum valor.
    
    pass
