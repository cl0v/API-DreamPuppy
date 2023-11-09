from fastapi import FastAPI,  HTTPException
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import json

app = FastAPI()


class PetModel(BaseModel):
    id: int
    breed: str # BreedId
    coverUrl: str
    # ... Todos os dados do pet.

class GalleryCardModel(BaseModel):
    id: int
    coverUrl: str



pets = [
    PetModel(id= 1, breed= "Pug", coverUrl= "https://i.imgur.com/ajzXLgu.jpeg"),
    PetModel(id= 2, breed= "Shih-Tzu", coverUrl= "https://i.imgur.com/jIFeQdT.jpeg"),
    PetModel(id= 3, breed= "Labrador", coverUrl= "https://i.imgur.com/4nusSJC.jpeg"),
]


@app.get('/gallery', response_model=list[GalleryCardModel])
def getGallery(amount: int = 9) -> list[GalleryCardModel]:
    if(amount > 30):
        raise  HTTPException(status_code=400, detail="Too many items")
    tmp = []
    for p in pets:
        tmp.append(GalleryCardModel(id=p.id, imageUrl=p.coverUrl))
    return tmp
