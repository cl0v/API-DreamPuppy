from sqlalchemy.orm import Session
from . import schemas, models


def add_breed(db: Session, breed: schemas.NewPuppy) -> models.BreedModel:
    new_breed = models.BreedModel(**breed.model_dump())
    db.add(new_breed)
    db.commit()
    db.refresh(new_breed)
    return new_breed


def add_puppy(db: Session, schema: schemas.NewPuppy) -> models.PuppyModel:
    db_puppy = models.PuppyModel(
        breed=schema.breed,
        price=schema.price,
        microchip=schema.microchip,
    )

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

    db.commit()

    return db_puppy


# def get_puppy(db: Session, puppy_id: int) -> PuppyModel:
#     raise Exception("Unimplemented")
