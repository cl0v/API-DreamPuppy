from .exceptions import GalleryException
from .schemas import GallerySchema
from fastapi import status

puppies = [
    GallerySchema(id=1, url="https://i.imgur.com/ajzXLgu.jpeg"),
    GallerySchema(id=2, url="https://i.imgur.com/jIFeQdT.jpeg"),
]


def get_puppies_cover_list(amount: int = 9) -> list[GallerySchema]:
    if amount > 30:
        raise GalleryException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Too many items",
        )
    tmp = []
    for p in puppies:
        tmp.append(GallerySchema(id=p.id, url=p.url))
    return tmp
