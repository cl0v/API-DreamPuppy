from pydantic import BaseModel


class GeoLoc(BaseModel):

    class ConfigDict:
        getter_dict = True


class CreateKennel(BaseModel):
    name: str
    phone: str
    instagram: str
    city: str
    uf: str
    address: str | None = None
    cep: str | None = None
    lat: float | None = None
    lon: float | None = None

    class ConfigDict:
        getter_dict = True


class OutputKennel(CreateKennel):
    id: int
    msg: str = "OK"


class OutputAddPuppy(BaseModel):
    id: int
    message: str = "OK"
