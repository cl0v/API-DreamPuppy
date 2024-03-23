from pydantic import BaseModel


class GeoLoc(BaseModel):
    lat: float
    lon: float

    class ConfigDict:
        getter_dict = True


class CreateKennel(BaseModel):
    name: str
    phone: str
    instagram: str
    city: str
    uf: str
    address: str
    cep: str
    geo: GeoLoc

    class ConfigDict:
        getter_dict = True


class OutputKennel(BaseModel):
    id: int
    geo: int


class OutputAddPuppy(BaseModel):
    id: int
    message: str = "OK"
