from pydantic import BaseModel


class Microchip(BaseModel):
    brand: str


class Vermifuges(BaseModel):
    brand: str
    date: str


class Vaccines(BaseModel):
    brand: str
    type: str
    date: str


class PuppySchema(BaseModel):
    id: int
    breed: int
    microchip: Microchip
    vermifuges: list[Vermifuges]
    vaccines: list[Vaccines]


class NewPuppySchema(BaseModel):
    breed: int
    microchip: Microchip
    vermifuges: list[Vermifuges]
    vaccines: list[Vaccines]


# Primeiro adicionar o filhote.
# Depois adicionar fotos.
# 2 ENDPOINTS

from sqlalchemy.sql import func

add_puppy_json = {
    # (id) Lulu da Pomerânia
    "breed": 1,
    "microchip": {"brand": "sim"},
    "vermifuges": [{"brand": "ENDAL® PLUS - MSD", "date": func.now()}],
    "vaccines": [{"brand": "Bio Max", "type": "V8", "date": func.now()}],
}
