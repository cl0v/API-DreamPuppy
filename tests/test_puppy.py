from . import test_main as main
from . import utils
import json
import pytest
from app.feat.puppy import schemas


ace_kennel_id = 2

def test_add_breed():
    r = main.client.post(
        "/breeds/new",
        content=json.dumps(add_breed_data),
        headers=main.admin_auth_header,
    )
    assert r.status_code == 200
    assert r.json()["name"] == add_breed_data["name"]
    assert r.json()["id"] > 0


def test_err_token_add_breed():
    r = main.client.post("/breeds/new", data=add_breed_data)
    assert r.status_code == 401
    assert r.is_client_error


def test_err_duplicate_add_breed():
    r = main.client.post(
        "/breeds/new",
        content=json.dumps(add_breed_data),
        headers=main.admin_auth_header,
    )
    assert r.status_code == 400
    assert r.json() == {"msg": "Raça já cadastrada"}
    assert r.is_client_error


def test_list_breeds():
    r = main.client.get("/breeds/list")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_get_puppy_from_id():
    r = main.client.get("/puppies/2")
    assert r.status_code == 200
    assert r.json()


def test_err_token_add_puppy():
    r = main.client.post(f"/kennels/{ace_kennel_id}/puppies/new")
    assert r.status_code == 401
    assert r.is_client_error


def test_err_fields_add_puppy():
    r = main.client.post(f"/kennels/{ace_kennel_id}/puppies/new", headers=main.admin_auth_header)
    assert r.status_code == 422
    assert r.is_client_error


def add_puppy():
    r =  main.client.post(
        f"/kennels/{ace_kennel_id}/puppies/new",
        headers=main.admin_auth_header,
        data=json.dumps(add_puppy_json),
    )
    print(r.json())
    assert r.status_code == 200
    d = r.json()
    assert "id" in d.keys()
    pid = d["id"]
    assert pid > 0
    return pid

def read_puppy(pid: int):
    r = main.client.get(f"/puppies/{pid}")
    assert r.status_code == 200
    return r

def test_add_n_read_puppy():
    pid = add_puppy()

    r2 = read_puppy(pid)
    
    d2 = r2.json()
    assert isinstance(add_puppy_json["breed"], int)
    assert isinstance(d2["breed"], str)
    d2.pop("breed")

    # assert "images" in d2.keys()
    # assert isinstance(d2["images"], list)
    # assert len(d2["images"]) == 1
    assert d2["id"] == pid

    for k in d2.keys():
        if k not in add_puppy_json.keys():
            continue
        try:
            inval = json.loads(add_puppy_json[k])
        except:
            inval = add_puppy_json[k]
        outval = d2[k]
        assert inval == outval


add_breed_data = {"name": "breed_{0}".format(utils.random_string_gen())}

some_available_breeds = [
    {"name": "Pug", "id": 1},
    {"name": "Labrador", "id": 2},
    {"name": "Teeste", "id": 3},
    {"name": "LULUZI", "id": 4},
    {"name": "LULUZ2I", "id": 5},
    {"name": "Lulu da pom", "id": 6},
]

add_puppy_json = {
    "breed": 1,
    "price": 970,
    "gender": -1,
    "pedigree": True,
    "birth": "2023-11-02T18:25:43.511000",
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
puppy_images = {
    "images": open("tests/blob/0.jpg", "rb"),
}
