from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    cpf: str


class UserWithToken(UserBase):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str
