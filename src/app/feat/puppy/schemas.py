from pydantic import BaseModel
from datetime import datetime
import json as json
from fastapi import UploadFile


class PuppyRequestForm (BaseModel):
    breed: int
    pedigree: bool
    microchip: bool
    minimum_age_departure_in_days: int | None = 60
    price: int
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
    id: int
    breed: int
    pedigree: bool
    price: int
    gender: int
    birth: datetime
    microchip: bool
    minimum_age_departure_in_days: int | None = None

    # Relational
    # vermifuges: list[Vermifuges] | None
    # vaccines: list[Vaccines] | None


class OutputPuppyWithBreedStr(OutPuppy):
    breed: str
    images: list[str]
