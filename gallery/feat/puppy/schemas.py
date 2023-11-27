from pydantic import BaseModel
from datetime import datetime


class NewBreed(BaseModel):
    name: str


class OutputBreed(NewBreed):
    id: int


class Vermifuges(BaseModel):
    brand: str
    date: datetime


class Vaccines(BaseModel):
    brand: str
    type: str
    date: datetime


class Media(BaseModel):
    url: str
    uploaded_at: datetime | None = None


class NewPuppy(BaseModel):
    breed: int
    microchip: bool
    minimum_age_departure_in_days: int | None = None
    price: int
    gender: int
    birth: datetime
    vermifuges: list[Vermifuges]
    vaccines: list[Vaccines]
    medias: list[Media]


class OutputPuppy(NewPuppy):
    id: int
    breed: str


# Primeiro adicionar o filhote.
# Depois adicionar fotos.
# 2 ENDPOINTS

from sqlalchemy.sql import func

add_puppy_json = {
    # (id) Lulu da Pomerânia
    "breed": 1,
    "microchip": True,
    "vermifuges": [{"brand": "ENDAL® PLUS - MSD", "date": func.now()}],
    "vaccines": [{"brand": "Bio Max", "type": "V8", "date": func.now()}],
}
