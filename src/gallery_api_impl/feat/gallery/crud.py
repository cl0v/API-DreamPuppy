from . import schemas  # , exceptions

# from fastapi import status
from sqlalchemy.orm import Session
from gallery_api_impl.feat.puppy.models import PuppyModel
from gallery_api_impl.feat.kennel.models import KennelModel
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page
from sqlalchemy import func

LIMIT_AMOUNT = 30
# Ja foi revisado pelos moderadores
REVIEWED_DEFAULT = True
# Está disponível para visualizar na galeria (public_access column)
VISIBLE_DEFAULT = True


def fill_gallery(
    db: Session, lat: float | None = None, lon: float | None = None
) -> Page[schemas.GallerySchema]:
    # TODO: Adicionar limitador de itens
    # if amount > LIMIT_AMOUNT:
    #     raise exceptions.GalleryException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         message="Too many items",
    #     )
    # select puppy,uuid from medias where puppy in (SELECT id FROM puppies WHERE puppies.reviewed=True AND puppies.public_access=True);

    # SELECT id FROM puppies WHERE puppies.reviewed=True AND puppies.public_access=True
    # stm = db.execute("SELECT SQRT(9)")

    q = (
        db.query(
            PuppyModel.id,
            PuppyModel.cover_url,
        )
        .join(
            KennelModel,
            KennelModel.id == PuppyModel.kennel,
        )
        .filter(
            PuppyModel.reviewed == REVIEWED_DEFAULT,
            PuppyModel.public_access == VISIBLE_DEFAULT,
            PuppyModel.cover_url.is_not(None),
        )
        # .group_by(
        #     PuppyModel.id,
        #     PuppyModel.cover_url,
        #     # KennelModel.lat,
        #     # KennelModel.lon,
        # )
        .order_by(
            func.sqrt(
                func.pow(KennelModel.lat - (lat), 2)
                + func.pow(KennelModel.lon - (lon), 2)
            ).asc(),
            PuppyModel.prio.desc(),
            PuppyModel.id.desc(),
        )
        # .limit(3)
        # .all()
    )

    # li = [{'id': id, 'url': get_gallery_image_url(media_uuid),} for id, media_uuid in q]

    val = paginate(
        db,
        q,
        transformer=lambda q: [{"id": id, "url": cover_url} for id, cover_url in q],
    )

    return val
