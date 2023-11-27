from pydantic import BaseModel


class CreateKennel(BaseModel):
    name: str
    phone: str
    instagram: str
    city: int
    address: str
    cep: str


class OutputKennel(CreateKennel):
    id: int


example_json = {
    "nome": "Canil DreamPuppy",
    "phone": "33998525199",
    "instagram": "dreampuppy.com.br",
    "city": 1,
    "address": "Avenida Olivia Flores",
    "cep": "39890000",
}
