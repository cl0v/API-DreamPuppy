from pydantic import BaseModel


# class ItemBase(BaseModel):
#     title: str
#     description: str | None = None


# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         from_attributes = True





class UserBase(BaseModel):
    full_name: str


class UserCreate(UserBase):
    cpf: str



class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
