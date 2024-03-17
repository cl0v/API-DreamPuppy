from pydantic import BaseModel
from datetime import datetime
import json as json


class PuppyRequestForm(BaseModel):
    breed: int
    price: int
    gender: int
    birth: datetime
    microchip: bool
    prio: int | None = 1
    weight: int | None = None
    pedigree: bool
    minimum_age_departure_in_days: int | None = 60

    class Config:
        orm_mode = True

class NewBreed(BaseModel):
    name: str


class OutputNewBreed(NewBreed):
    id: int


class Vermifuges(BaseModel):
    brand: str
    date: datetime


class Vaccines(BaseModel):
    brand: str
    type: str
    date: datetime


class OutPuppy(BaseModel):
    # Trazer o images pra ca e todo filhote retornado irá ter uma lista de fotos. [task 213123312321]
    # images: list[str]
    id: int
    breed: int
    pedigree: bool
    price: int
    gender: int
    birth: datetime
    microchip: bool
    weight: int
    minimum_age_departure_in_days: int | None = None

    # Relational
    # vermifuges: list[Vermifuges] | None
    # vaccines: list[Vaccines] | None


class OutputPuppyWithBreedStr(OutPuppy):
    breed: str
    images: list[str]
