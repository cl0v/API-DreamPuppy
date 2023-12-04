from pydantic import BaseModel
from typing import Annotated
from fastapi.param_functions import Form
from datetime import datetime
import json as json


class PuppyRequestForm:
    def __init__(
        self,
        *,
        breed: Annotated[int, Form()],
        pedigree: Annotated[bool, Form()],
        microchip: Annotated[bool, Form()],
        minimum_age_departure_in_days: Annotated[int | None, Form()] = 60,
        price: Annotated[int, Form()],
        gender: Annotated[int, Form()],
        birth: Annotated[datetime, Form()],
        # Relational
        vermifuges: Annotated[str | None, Form()],
        vaccines: Annotated[str | None, Form()],
    ):
        self.breed = breed
        self.pedigiree = pedigree
        self.microchip = microchip
        self.minimum_age_departure_in_days = minimum_age_departure_in_days
        self.price = price
        self.gender = gender
        self.birth = birth
        self.vermifuges = vermifuges
        self.vaccines = vaccines


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
    vermifuges: list[Vermifuges] | None
    vaccines: list[Vaccines] | None


class OutputPuppyWithBreedStr(OutPuppy):
    breed: str
    images: list[str]
