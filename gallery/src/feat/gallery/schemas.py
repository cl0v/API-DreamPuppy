from pydantic import BaseModel


class GallerySchema(BaseModel):
    id: int
    url: str
    gender: int  # -1 fêmea, 1 macho, 0 Nil
