from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import json

app = FastAPI()


class PetModel(BaseModel):
    id: int
    breed: str  # BreedId
    coverUrl: str
    # ... Todos os dados do pet.


pets = [
    PetModel(id=1, breed="Pug", coverUrl="https://i.imgur.com/ajzXLgu.jpeg"),
    PetModel(id=2, breed="Shih-Tzu", coverUrl="https://i.imgur.com/jIFeQdT.jpeg"),
    PetModel(id=3, breed="Labrador", coverUrl="https://i.imgur.com/4nusSJC.jpeg"),
    PetModel(id=4, breed="Pug", coverUrl="https://i.imgur.com/ajzXLgu.jpeg"),
    PetModel(id=5, breed="Shih-Tzu", coverUrl="https://i.imgur.com/jIFeQdT.jpeg"),
    PetModel(id=6, breed="Labrador", coverUrl="https://i.imgur.com/4nusSJC.jpeg"),
    PetModel(id=7, breed="Labrador", coverUrl="https://i.imgur.com/4nusSJC.jpeg"),
    PetModel(id=8, breed="Pug", coverUrl="https://i.imgur.com/ajzXLgu.jpeg"),
    PetModel(id=9, breed="Shih-Tzu", coverUrl="https://i.imgur.com/jIFeQdT.jpeg"),
    PetModel(id=10, breed="Pug", coverUrl="https://i.imgur.com/ajzXLgu.jpeg"),
]


class CanilModel(BaseModel):
    id: int
    phone: str
    instagram: str = None
    facebook: str = None
    site: str = None
    other: str = None  # Não criar ref no banco de dados até ter usos válidos.
    # ... ADICIONAR várias formas de contato. (other: str = None)


# Implementar REGRA: O telefone sempre deve começar com 55.
## Talvez uma regra temporária. Conferir se o dd pertence a região implementada. (77, ou proximos)

# Fazer com regex? Só mais tarde cumpadi.
canis = [
    CanilModel(id=1, phone="5572123456789"),
    CanilModel(id=2, phone="5572123456789"),
    CanilModel(id=3, phone="5572123456789"),
]


class GalleryCardModel(BaseModel):
    id: int
    coverUrl: str


@app.get("/gallery", response_model=list[GalleryCardModel])
def getGallery(amount: int = 9) -> list[GalleryCardModel]:
    if amount > 30:
        raise HTTPException(status_code=400, detail="Too many items")
    tmp = []
    for p in pets:
        tmp.append(GalleryCardModel(id=p.id, coverUrl=p.coverUrl))
    return tmp


## Pagina de Auth (Após modulo de segurança)


## Pagina de detalhes do canil.
@app.get("/canil",)
def fetchCanilById(canil_id: str | None):
    if not canil_id:
        return {}
    return {
        "id": canil_id,
        "dev": True,
        "name": "Canil Beira Rio",
        "address": "Salvador - BA",
        "phone": "5533998525199",
        "whatsapp": "5533998525199",
        "instagram": "dreampuppy.com.br",
    }



## Pagina de detalhes do filhote.
