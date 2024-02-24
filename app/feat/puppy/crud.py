from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from app.feat.puppy import schemas, models, exceptions
from fastapi import status, UploadFile
import json
from datetime import datetime
import uuid
from app.feat.puppy.image_storage import upload_image, get_image_public_url
from app.feat.kennel.models import KennelsNPuppies

# from app.feat.puppy.azure_storage import  get_url_by_key, create_container


def add_breed(db: Session, breed: schemas.NewBreed) -> models.BreedModel:
    new_breed = models.BreedModel(**breed.model_dump())
    try:
        db.add(new_breed)
        db.commit()
        db.refresh(new_breed)
    except IntegrityError:
        raise exceptions.PuppyDetailsException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Raça já cadastrada",
        )
    return new_breed


def list_breeds(db: Session) -> list[models.BreedModel]:
    return db.query(models.BreedModel).all()


def add_puppy(
    db: Session,
    images: list[UploadFile],
    schema: schemas.PuppyRequestForm,
) -> models.PuppyModel:
    puppy_uuid = uuid.uuid4().hex
    db_puppy = models.PuppyModel(
        uuid=puppy_uuid,
        breed=schema.breed,
        pedigree=schema.pedigiree,
        microchip=schema.microchip,
        price=schema.price,
        birth=schema.birth,
        gender=schema.gender,
        minimum_age_departure_in_days=schema.minimum_age_departure_in_days,
    )

    jsonVerm = json.loads(schema.vermifuges)
    tmpListVerm: list[models.Vermifuge] = []
    for j in jsonVerm:
        j["date"] = datetime.fromisoformat(j["date"])
        db_vermifuge = models.Vermifuge(
            **j,
        )
        tmpListVerm.append(db_vermifuge)

    jsonVacc = json.loads(schema.vaccines)
    tmpListVacc: list[models.Vaccine] = []
    for j in jsonVacc:
        j["date"] = datetime.fromisoformat(j["date"])
        db_vaccine = models.Vaccine(
            **j,
        )
        tmpListVacc.append(db_vaccine)

    # 1 unico container por iamgem
    # create_container(puppy_uuid)
    tmpImgs: list[models.Media] = []
    for image in images["images"]:
        db_media: models.Media = _upload_media(image, puppy_uuid)
        tmpImgs.append(db_media)

    # 1st important
    db.add(db_puppy)
    db.commit()
    db.refresh(db_puppy)

    # 2nd important
    for m in tmpImgs:
        m.puppy = db_puppy.id
        db.add(m)
        db.commit()

    # 3rd and so on... importance
    for m in tmpListVerm:
        m.puppy = db_puppy.id
        db.add(m)
    for m in tmpListVacc:
        m.puppy = db_puppy.id
        db.add(m)

    db.commit()

    return db_puppy


def _upload_media(img: UploadFile, puppy_uuid: str) -> models.Media:
    # O upload_image precisa retornar o id para que seja salvo.
    img_id = upload_image(img, puppy_uuid)
    model = models.Media(uuid=img_id)
    return model


def get_puppy(db: Session, puppy_id: int) -> models.PuppyModel:
    puppy = (
        db.query(models.PuppyModel)
        .options(
            joinedload(models.PuppyModel.vaccines),
            joinedload(models.PuppyModel.vermifuges),
            joinedload(models.PuppyModel.images),
        )
        .filter(models.PuppyModel.id == puppy_id)
        .first()
    )

    if not puppy:
        raise exceptions.PuppyDetailsException(
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

    d["breed"] = breed.name

    d["images"] = [get_image_public_url(i.uuid) for i in images]

    return d


def get_kennel_id_from_puppy_id(db: Session, puppy_id: str) -> int:
    q = db.query(KennelsNPuppies).filter(KennelsNPuppies.puppy_id == puppy_id).first()
    if not q:
        raise exceptions.PuppyDetailsException(
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
    if(not puppy.reviewed):
        puppy.reviewed = True
    if(not puppy.public_access):
        puppy.public_access = True
    
    db.commit()
    return puppy_id


def hide_from_gallery(
    db: Session,
    puppy_id: int,
) -> int:
    puppy = db.query(models.PuppyModel).filter(models.PuppyModel.id == puppy_id).first()
    if(puppy.reviewed):
        puppy.reviewed = False
    if(puppy.public_access):
        puppy.public_access = False
        
    db.commit()
    return puppy_id
