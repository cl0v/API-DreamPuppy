from pydantic import BaseModel
from datetime import datetime
import json as json


class PuppyRequestForm(BaseModel):
    breed: int
    price: int
    pedigree: bool
    microchip: bool
    weight: int | None = None
    minimum_age_departure_in_days: int | None = 60
    gender: int
    birth: datetime


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
    weight: int | None
    gender: int
    birth: datetime
    microchip: bool
    minimum_age_departure_in_days: int | None

    # Relational
    # vermifuges: list[Vermifuges] | None
    # vaccines: list[Vaccines] | None


class OutputPuppyWithBreedStr(OutPuppy):
    breed: str
    images: list[str]
