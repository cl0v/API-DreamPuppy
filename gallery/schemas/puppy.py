from pydantic import BaseModel


class Microchip(BaseModel):
    brand: str
    number: str


class Vermifuges(BaseModel):
    brand: str
    date: str


class Vaccines(BaseModel):
    brand: str
    type: str
    date: str


class PuppyBase(BaseModel):
    breed: int
    microchip: Microchip
    vermifuges: list[Vermifuges]
    vaccines: list[Vaccines]


# Primeiro adicionar o filhote.
# Depois adicionar fotos.
# 2 ENDPOINTS

from sqlalchemy.sql import func

add_puppy_json = {
    "breed": 1,  # (id) Lulu da Pomerânia
    "microchip": {"brand": "sim"},
    "vermifuges": [{"brand": "ENDAL® PLUS - MSD", "date": func.now()}],
    "vaccines": [{"brand": "Bio Max", "type": "V8", "date": func.now()}],
}
