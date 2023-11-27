from pydantic import BaseModel
from datetime import datetime


class Vermifuges(BaseModel):
    brand: str
    date: datetime


class Vaccines(BaseModel):
    brand: str
    type: str
    date: datetime


# class PuppySchema(BaseModel):
#     id: int
#     breed: int
#     # microchip: Microchip
#     # vermifuges: list[Vermifuges]
#     # vaccines: list[Vaccines]


class NewPuppy(BaseModel):
    breed: int
    microchip: bool
    price: int
    vermifuges: list[Vermifuges]
    vaccines: list[Vaccines]


class OutputPuppy(NewPuppy):
    id: int


class NewBreed(BaseModel):
    name: str


class OutputBreed(NewBreed):
    id: int


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
