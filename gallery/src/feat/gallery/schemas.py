from pydantic import BaseModel


class GallerySchema(BaseModel):
    id: int
    url: str
    # gender: int = 0  # -1 fêmea, 1 macho, 0 Nil
