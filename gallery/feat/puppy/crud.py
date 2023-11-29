from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from . import schemas, models, exceptions
from fastapi import status, UploadFile
import json
from datetime import datetime
import uuid
from gallery.storage import create_container, create_blob, upload_blob


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
) -> schemas.OutPuppy:
    container = uuid.uuid4().hex
    db_puppy = models.PuppyModel(
        container=container,
        breed=schema.breed,
        microchip=schema.microchip,
        price=schema.price,
        birth=schema.birth,
        gender=schema.gender,
        minimum_age_departure_in_days=schema.minimum_age_departure_in_days,
    )

    db.add(db_puppy)
    db.commit()
    db.refresh(db_puppy)

    jsonVerm = json.loads(schema.vermifuges)

    for j in jsonVerm:
        j["date"] = datetime.fromisoformat(j["date"])
        db_vermifuge = models.Vermifuge(
            **j,
            puppy=db_puppy.id,
        )
        db.add(db_vermifuge)

    jsonVacc = json.loads(schema.vaccines)
    for j in jsonVacc:
        j["date"] = datetime.fromisoformat(j["date"])
        db_vaccine = models.Vaccine(
            **j,
            puppy=db_puppy.id,
        )
        db.add(db_vaccine)

    create_container(container)

    for image in images["images"]:
        media = _upload_media(image, db_puppy.id, container)
        db.add(media)

    db.commit()
    return db_puppy


def _upload_media(img: UploadFile, puppy: int, container: str) -> models.Media:
    blob_id = uuid.uuid4().hex
    blob = create_blob(blob_id, container, img.content_type)

    upload_blob(blob, img.file, img.content_type)
    model = models.Media(
        url=blob.primary_endpoint,
        puppy=puppy,
        blob=blob_id,
    )
    return model


def get_puppy(db: Session, puppy_id: int) -> models.PuppyModel:
    model = (
        db.query(models.PuppyModel)
        .options(
            joinedload(models.PuppyModel.vaccines),
            joinedload(models.PuppyModel.vermifuges),
            joinedload(models.PuppyModel.medias),
        )
        .filter(models.PuppyModel.id == puppy_id)
        .first()
    )

    if not model:
        raise exceptions.PuppyDetailsException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Nenhum filhote encontrado.",
        )

    breed = (
        db.query(models.BreedModel)
        .filter(
            models.BreedModel.id == model.breed,
        )
        .first()
    )

    d = model.__dict__

    d["breed"] = breed.name
    return d


def list_puppies(
    db: Session,
    puppies_ids: list[int],
) -> list[models.PuppyModel]:
    return (
        db.query(models.PuppyModel)
        .filter(
            models.PuppyModel.id.in_(
                puppies_ids,
            )
        )
        .all()
    )
