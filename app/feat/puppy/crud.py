from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError, DatabaseError
from app.feat.puppy import schemas, models, exceptions
from fastapi import status, UploadFile
import json
from datetime import datetime
import uuid
from app.feat.puppy.image_storage import (
    upload_image,
    get_image_public_url,
    get_gallery_image_url,
)
from app.feat.kennel.models import KennelsNPuppies

# from app.feat.puppy.azure_storage import  get_url_by_key, create_container


def add_breed(db: Session, breed: schemas.NewBreed) -> models.BreedModel:
    new_breed = models.BreedModel(**breed.model_dump())
    try:
        db.add(new_breed)
        db.commit()
        db.refresh(new_breed)
    except IntegrityError:
        raise exceptions.PuppyException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Raça já cadastrada",
        )
    return new_breed


def list_breeds(db: Session) -> list[models.BreedModel]:
    return db.query(models.BreedModel).all()


def add_puppy_images(db: Session, images: list[UploadFile], puppy_id: int, setCover: bool):
    # create_container(puppy_uuid)
    tmpImgs: list[models.Media] = []
    for image in images["images"]:
        db_media: models.Media = _upload_media(image, puppy_id)
        tmpImgs.append(db_media)

    ids: list[int] = []
    for m in tmpImgs:
        m.puppy = puppy_id
        db.add(m)
        db.commit()
        ids.append(m.id)
    
    if setCover:
        update_cover_url(db, puppy_id=puppy_id, linkToId = ids[0])
    
    return ids


def update_cover_url(db: Session, puppy_id: int, linkToId: int):
    # Buscar o link do small gallery
    coverImageUuid = (
        db.query(models.Media.uuid).where(models.Media.id == linkToId).first()
    )
    if not coverImageUuid:
        raise exceptions.MediaException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Arquivo de mídia não existe.",
        )

    coverImageUuid = coverImageUuid.uuid

    coverUrl = get_gallery_image_url(coverImageUuid)

    duplicateCoverAlert = (
        db.query(models.PuppyModel)
        .where(models.PuppyModel.cover_url == coverUrl)
        .first()
    )

    if duplicateCoverAlert:
        raise exceptions.PuppyException(
            status_code=status.HTTP_409_CONFLICT,
            message="Imagem já linkada a outro filhote.",
        )

    puppy = db.query(models.PuppyModel).filter(models.PuppyModel.id == puppy_id).first()

    if not puppy:
        raise exceptions.PuppyException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Filhote não existe.",
        )

    puppy.cover_url = coverUrl

    db.commit()

    return


def add_puppy(
    db: Session,
    schema: schemas.PuppyRequestForm,
) -> models.PuppyModel:
    # TODO: Verificar se a raça existe na lista de raças.

    #     sqlalchemy.exc.IntegrityError: (psycopg2.errors.ForeignKeyViolation) insert or update on table "puppies" violates foreign key constraint "puppies_breed_fkey"
    #     DETAIL:  Key (breed)=(25) is not present in table "breeds".

    puppy_uuid = uuid.uuid4().hex
    db_puppy = models.PuppyModel(
        uuid=puppy_uuid,
        breed=schema.breed,
        pedigree=schema.pedigree,
        microchip=schema.microchip,
        price=schema.price,
        birth=schema.birth,
        gender=schema.gender,
        minimum_age_departure_in_days=schema.minimum_age_departure_in_days,
    )

    # jsonVerm = json.loads(schema.vermifuges)
    # tmpListVerm: list[models.Vermifuge] = []
    # for j in jsonVerm:
    #     j["date"] = datetime.fromisoformat(j["date"])
    #     db_vermifuge = models.Vermifuge(
    #         **j,
    #     )
    #     tmpListVerm.append(db_vermifuge)

    # jsonVacc = json.loads(schema.vaccines)
    # tmpListVacc: list[models.Vaccine] = []
    # for j in jsonVacc:
    #     j["date"] = datetime.fromisoformat(j["date"])
    #     db_vaccine = models.Vaccine(
    #         **j,
    #     )
    #     tmpListVacc.append(db_vaccine)

    try:
        # 1st important
        db.add(db_puppy)
        db.flush()
        db.commit()
        db.refresh(db_puppy)
    except DatabaseError as err:
        # Maybe this can be rlly unsafe
        db.rollback()
        raise err

    # 3rd and so on... importance
    # for m in tmpListVerm:
    #     m.puppy = db_puppy.id
    #     db.add(m)
    # for m in tmpListVacc:
    #     m.puppy = db_puppy.id
    #     db.add(m)

    return db_puppy


def _upload_media(img: UploadFile, puppy_uuid: str) -> models.Media:
    # O upload_image precisa retornar o id para que seja salvo.
    img_id = upload_image(img, puppy_uuid)
    model = models.Media(uuid=img_id)
    return model


def get_puppy(db: Session, puppy_id: int):
    puppy = (
        db.query(models.PuppyModel)
        .options(
            # joinedload(models.PuppyModel.vaccines),
            # joinedload(models.PuppyModel.vermifuges),
            joinedload(models.PuppyModel.images),
        )
        .filter(models.PuppyModel.id == puppy_id)
        .first()
    )

    if not puppy:
        raise exceptions.PuppyException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Nenhum filhote encontrado.",
        )

    breed = (
        db.query(models.BreedModel)
        .filter(
            models.BreedModel.id == puppy.breed,
        )
        .first()
    )

    images = (
        db.query(models.Media)
        .filter(
            models.Media.puppy == puppy.id,
        )
        .all()
    )

    d = puppy.__dict__

    # d["vaccines"] = d["vaccines"].all()

    d["breed"] = breed.name

    d["images"] = [get_image_public_url(i.uuid) for i in images]

    return d


def get_kennel_id_from_puppy_id(db: Session, puppy_id: str) -> int:
    q = db.query(KennelsNPuppies).filter(KennelsNPuppies.puppy_id == puppy_id).first()
    if not q:
        raise exceptions.PuppyException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Canil não encontrado.",
        )
    return q.kennel_id


def list_puppies(
    db: Session,
    puppies_ids: list[int],
) -> list[models.PuppyModel]:
    return (
        db.query(models.PuppyModel).filter(models.PuppyModel.id.in_(puppies_ids)).all()
    )


def show_on_gallery(
    db: Session,
    puppy_id: int,
) -> int:
    puppy = db.query(models.PuppyModel).filter(models.PuppyModel.id == puppy_id).first()
    if not puppy.reviewed:
        puppy.reviewed = True
    if not puppy.public_access:
        puppy.public_access = True

    db.commit()
    return puppy_id


def hide_from_gallery(
    db: Session,
    puppy_id: int,
) -> int:
    puppy = db.query(models.PuppyModel).filter(models.PuppyModel.id == puppy_id).first()
    if puppy.reviewed:
        puppy.reviewed = False
    if puppy.public_access:
        puppy.public_access = False

    db.commit()
    return puppy_id
