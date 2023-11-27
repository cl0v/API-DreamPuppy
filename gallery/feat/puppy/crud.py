from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from . import schemas, models, exceptions
from fastapi import status


def add_breed(db: Session, breed: schemas.NewPuppy) -> models.BreedModel:
    new_breed = models.BreedModel(**breed.model_dump())
    try:
        db.add(new_breed)
        db.commit()
        db.refresh(new_breed)
    except IntegrityError as err:
        raise exceptions.PuppyDetailsException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Raça já cadastrada",
        )
    return new_breed


def add_puppy(db: Session, schema: schemas.NewPuppy) -> models.PuppyModel:
    db_puppy = models.PuppyModel(schema.dict())
    #     breed=schema.breed,
    #     price=schema.price,
    #     microchip=schema.microchip,
    # )

    db.add(db_puppy)
    db.commit()
    db.refresh(db_puppy)

    for vermifuge in schema.vermifuges:
        db_vermifuge = models.Vermifuge(
            **vermifuge.model_dump(),
            puppy=db_puppy.id,
        )
        db.add(db_vermifuge)

    for vaccine in schema.vaccines:
        db_vaccine = models.Vaccine(
            **vaccine.model_dump(),
            puppy=db_puppy.id,
        )
        db.add(db_vaccine)

    for media in schema.medias:
        db_media = models.Media(
            **media.model_dump(),
            puppy=db_puppy.id,
        )
        db.add(db_media)

    db.commit()

    return db_puppy


def get_puppy(db: Session, puppy_id: int) -> models.PuppyModel:
    print('Entrou??')
    
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

    breed = (
        db.query(models.BreedModel).filter(models.BreedModel.id == model.breed).first()
    )

    d = model.__dict__

    d["breed"] = breed.name
    return d


