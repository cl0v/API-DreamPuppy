from .. import utils

ace_kennel_id = 2

add_breed_data = {"name": "breed_{0}".format(utils.random_string_gen())}

some_available_breeds = [
    {"name": "Pug", "id": 1},
    {"name": "Labrador", "id": 2},
    {"name": "Lulu da Pomerânia", "id": 6},
]

add_puppy_json = {
    "breed": 1,
    "price": 970,
    "gender": -1,
    "pedigree": True,
    "birth": "2023-11-02T18:25:43",
    "microchip": True,
    "minimum_age_departure_in_days": 60,
    # "vermifuges": json.dumps(
    #     [
    #         {
    #             "brand": "HBO",
    #             "date": "2023-11-22T18:25:43.511000",
    #         },
    #     ],
    # ),
    # "vaccines": json.dumps(
    #     [
    #         {
    #             "brand": "Bio Max",
    #             "type": "V8",
    #             "date": "2023-11-23T18:25:43.511000",
    #         },
    #     ]
    # ),
}

# l = [f for f in os.listdir("./imgs")]
# puppy_images = {
#     "images": open("blob/0.jpg", "rb"),
# }
