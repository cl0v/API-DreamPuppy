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
        from_attributes = True


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
    weight: int | None
    minimum_age_departure_in_days: int | None = None

    # Relational
    # vermifuges: list[Vermifuges] | None
    # vaccines: list[Vaccines] | None


class OutPuppyDetails(OutPuppy):
    breed: str
    images: list[str] | None


class InInUpdatePuppyDetails(BaseModel):
    breed: int | None = None
    pedigree: bool | None = None
    price: int | None = None
    microchip: bool | None = None
    weight: int | None = None

    class Config:
        from_attributes = True

    #     data =
    # (exclude_unset=True)
