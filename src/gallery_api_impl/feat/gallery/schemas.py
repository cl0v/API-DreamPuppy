from pydantic import BaseModel


class GallerySchema(BaseModel):
    id: int
    url: str
    # geo: dict[str, float]
    # extras: str
