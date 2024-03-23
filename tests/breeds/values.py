from gallery_api_impl.constants.strings import DUPLICATED_BREED_ERROR
from ..utils import random_string_gen

breed_json = {"name": "Labrador"}

expected_response_json = {"id": 31, "msg": DUPLICATED_BREED_ERROR}

new_random_breed_json = {"name": "breed_{0}".format(random_string_gen())}
