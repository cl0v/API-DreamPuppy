from pydantic import BaseModel


class GallerySchema(BaseModel):
    id: int
    # TODO: Implementar o url da imagem da tumb. (Pode ser imagem reduzida para 512x512)
    # url: str
