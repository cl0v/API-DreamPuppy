from pydantic import BaseModel


class GallerySchema(BaseModel):
    id: int
    uuid: str
    url: str
    # geo: dict[str, float]
    # extras: str
