from pydantic import BaseModel


class GallerySchema(BaseModel):
    id: int
    url: str
    # extras: str
