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
    email: str
    full_name: str


class UserCreate(UserBase):
    password: str
    cpf: str



class User(UserBase):
    id: int
    is_active: bool
    # items: list[Item] = []

    class Config:
        from_attributes = True
