from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError, DatabaseError
from gallery_api_impl.feat.puppy import schemas, models, exceptions
from fastapi import status, UploadFile
from gallery_api_impl.constants.strings import (
    DUPLICATED_BREED_ERROR,
    KENNEL_NOT_FOUND_ERROR,
    PUPPY_NOT_FOUND_ERROR,
    PUPPIES_NOT_FOUND_ERROR,
    IMAGE_ALREADY_TAKEN_ERROR,
    MEDIA_NOT_FOUND_ERROR,
)
import uuid
from gallery_api_impl.feat.puppy.image_storage import (
    upload_image,
    get_gallery_image_url,
)

from typing import Union


def add_breed(db: Session, breed: schemas.NewBreed) -> models.BreedModel:
    # Verifica se a raça já está cadastrada
    breedAlreadyRegistered: models.BreedModel | None = (
        db.query(models.BreedModel).where(models.BreedModel.name == breed.name).first()
    )
    if breedAlreadyRegistered is not None:
        raise exceptions.PuppyException(
            status_code=status.HTTP_409_CONFLICT,
            message=DUPLICATED_BREED_ERROR,
            puppy_id=breedAlreadyRegistered.id,
        )

    new_breed = models.BreedModel(**breed.model_dump())

    try:
        db.add(new_breed)
        db.commit()
        db.refresh(new_breed)
    except IntegrityError as err:
        print(err._message)
        raise exceptions.PuppyException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=DUPLICATED_BREED_ERROR,
        )
    return new_breed


def list_breeds(db: Session) -> list[models.BreedModel]:
    return db.query(models.BreedModel).all()


def add_puppy_images(
    db: Session, images: list[UploadFile], puppy_id: int, setCover: bool
):
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
        update_cover_url(db, puppy_id=puppy_id, linkToId=ids[0])

    return ids


def update_cover_url(db: Session, puppy_id: int, linkToId: int):
    # Buscar o link do small gallery
    coverImageUuid = (
        db.query(models.Media.uuid).where(models.Media.id == linkToId).first()
    )
    if not coverImageUuid:
        raise exceptions.MediaException(
            status_code=status.HTTP_404_NOT_FOUND,
            message=MEDIA_NOT_FOUND_ERROR,
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
            message=IMAGE_ALREADY_TAKEN_ERROR,
        )

    puppy = db.query(models.PuppyModel).filter(models.PuppyModel.id == puppy_id).first()

    if not puppy:
        raise exceptions.PuppyException(
            status_code=status.HTTP_404_NOT_FOUND,
            message=PUPPY_NOT_FOUND_ERROR,
        )

    puppy.cover_url = coverUrl

    db.commit()

    return


def add_puppy(
    db: Session,
    schema: schemas.PuppyRequestForm,
    kennel_id: int,
) -> models.PuppyModel:
    # TODO: Verificar se a raça existe na lista de raças.

    #     sqlalchemy.exc.IntegrityError: (psycopg2.errors.ForeignKeyViolation) insert or update on table "puppies" violates foreign key constraint "puppies_breed_fkey"
    #     DETAIL:  Key (breed)=(25) is not present in table "breeds".

    puppy_uuid = uuid.uuid4().hex

    db_puppy = models.PuppyModel(
        **schema.model_dump(),
        uuid=puppy_uuid,
        kennel=kennel_id,
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
    img_id, public_url = upload_image(img, puppy_uuid)
    model = models.Media(uuid=img_id, public_url=public_url)
    return model


def update_puppy(
    db: Session,
    puppy: schemas.InpUpdatePuppyDetails,
    puppy_id: int,
) -> schemas.OutPuppy:
    raise NotImplementedError("Implementar atualização dos dados do filhote!")
    db_puppy = (
        db.query(models.PuppyModel)
        .filter(
            models.PuppyModel.id == puppy_id,
        )
        .first()
    )

    # puppy.model_dump(exclude_unset=True)
    # db_puppy.weight = 3000
    db.add(db_puppy)
    db.commit()
    db.refresh(db_puppy)
    return db_puppy


def get_puppy(db: Session, puppy_id: Union[int,str]):
    puppy = None
    
    if puppy_id.isnumeric():
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
    else:
        puppy = (
            db.query(models.PuppyModel)
            .options(
                # joinedload(models.PuppyModel.vaccines),
                # joinedload(models.PuppyModel.vermifuges),
                joinedload(models.PuppyModel.images),
            )
            .filter(models.PuppyModel.uuid == puppy_id)
            .first()
        )

    if not puppy:
        raise exceptions.PuppyException(
            status_code=status.HTTP_404_NOT_FOUND,
            message=PUPPIES_NOT_FOUND_ERROR,
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

    d["images"] = []
    for i in images:
        if i.public_url is None:
            continue
        else:
            d["images"].append(i.public_url)

    # d["vaccines"] = d["vaccines"].all()

    d["breed"] = breed.name

    return d


def get_kennel_id_from_puppy_id(db: Session, puppy_id: str) -> int:
    q = (
        db.query(models.PuppyModel.kennel)
        .filter(models.PuppyModel.id == puppy_id)
        .first()
    )
    if not q:
        raise exceptions.PuppyException(
            status_code=status.HTTP_404_NOT_FOUND,
            message=KENNEL_NOT_FOUND_ERROR,
        )
    return q.kennel


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
