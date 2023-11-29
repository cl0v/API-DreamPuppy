from pydantic import BaseModel


class CreateKennel(BaseModel):
    name: str
    phone: str
    instagram: str
    city: str
    uf: str
    address: str
    cep: str


class OutputKennel(CreateKennel):
    id: int
