from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    cpf: str


class UserWithToken(UserBase):

    access_token: str
    token_type: str
    
    class ConfigDict:
        getter_dict = True
