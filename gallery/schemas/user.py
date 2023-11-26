from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    cpf: str


class User(UserBase):
    id: int
    # is_active: bool

    class Config:
        from_attributes = True

class UserWithToken(User):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str