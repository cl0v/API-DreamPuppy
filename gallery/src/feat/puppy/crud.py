from sqlalchemy.orm import Session
from . import schemas, models


def add_breed(db: Session, breed: schemas.NewPuppy) -> models.BreedModel:
    new_breed = models.BreedModel(**breed.model_dump())
    db.add(new_breed)
    db.commit()
    db.refresh(new_breed)
    return new_breed


def add_puppy(db: Session, schema: schemas.NewPuppy) -> models.PuppyModel:
    # # Criando objetos Vaccine
    # vaccines = [vaccine_data.model_dump() for vaccine_data in schema.vaccines]

    # # Criando objetos Vermifuge
    # vermifuges = [vermifuge_data.model_dump() for vermifuge_data in schema.vermifuges]

    # Criando o PuppyModel com os objetos relacionados
    dump = schema.model_dump()
    db_puppy = models.PuppyModel(**dump)

    db.add(db_puppy)
    db.commit()
    db.refresh(db_puppy)
    return db_puppy


# def get_puppy(db: Session, puppy_id: int) -> PuppyModel:
#     raise Exception("Unimplemented")
