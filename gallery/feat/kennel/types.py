from typing import Annotated
from fastapi.param_functions import Form


class PuppyRequestForm:
    def __init__(
        self,
        *,
        breed: Annotated[str, Form()],
        age: Annotated[int, Form()],
    ):
        self.breed = breed
        self.age = age
