from sqlalchemy.orm import Session
from .schemas import PuppySchema, NewPuppySchema, NewBreedSchema
from .models import BreedModel


# def add_puppy(db: Session, schema: NewPuppySchema) -> PuppyModel:
#     # Criando o objeto Microchip
#     microchip = schema.microchip.model_dump()

#     db.add(Microchip(b))

#     # Criando objetos Vaccine
#     vaccines = [vaccine_data.model_dump() for vaccine_data in schema.vaccines]

#     # Criando objetos Vermifuge
#     vermifuges = [vermifuge_data.model_dump() for vermifuge_data in schema.vermifuges]

#     # Criando o PuppyModel com os objetos relacionados
#     db_puppy = PuppyModel(
#         breed=schema.breed,
#         microchip=microchip,
#         vaccines=vaccines,
#         vermifuges=vermifuges,
#     )

#     db.add(db_puppy)
#     db.commit()
#     db.refresh(db_puppy)
#     return db_puppy


# def get_puppy(db: Session, puppy_id: int) -> PuppyModel:
#     raise Exception("Unimplemented")


def add_breed(db: Session, breed: NewBreedSchema) -> BreedModel:
    new_breed = BreedModel(**breed.model_dump())
    db.add(new_breed)
    db.commit()
    db.refresh(new_breed)
    return new_breed
