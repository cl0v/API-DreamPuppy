from starlette.testclient import TestClient
from main import app
import pytest
import json
import string
import random
import os

# Tests: Gallery / Details / Kennel

def random_string_gen(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


client = TestClient(app)


def test_fill_gallery():
    response = client.get("/gallery")
    assert response.status_code == 200
    for a in some_gallery_data:
        assert a in response.json()


def test_token_add_breed():
    r = client.post("/breeds/new", data=add_breed_data)
    assert r.status_code == 401
    assert r.is_client_error


def test_add_breed():
    r = client.post(
        "/breeds/new",
        data=json.dumps(add_breed_data),
        headers=admin_auth_header,
    )
    assert r.status_code == 200
    assert r.json()['name'] == add_breed_data['name']
    assert r.json()['id'] > 0


def test_duplicate_add_breed():
    r = client.post(
        "/breeds/new",
        data=json.dumps(add_breed_data),
        headers=admin_auth_header,
    )
    assert r.status_code == 400
    assert r.json() == {"msg": "Raça já cadastrada"}
    assert r.is_client_error


def test_list_breeds():
    r = client.get("/breeds/list")
    assert r.status_code == 200
    for a in some_available_breeds:
        assert a in r.json()


def test_get_kennel():
    r = client.get("/kennels/7")
    assert r.status_code == 200
    assert r.json() == kennel7


def test_token_list_puppies_from_kennel():
    r = client.get("/kennels/4/puppies/")
    assert r.status_code == 401
    assert r.is_client_error


def test_list_puppies_from_kennel():
    r = client.get("/kennels/4/puppies/", headers=admin_auth_header)
    assert r.status_code == 200
    for v in  puppies_from_kennel4:
        assert v in r.json()


def test_empty_list_puppies_from_kennel():
    r = client.get("/kennels/2/puppies/", headers=admin_auth_header)
    assert r.status_code == 200
    assert r.json() == []


def test_get_puppy_from_id():
    r = client.get("/puppies/2")
    assert r.status_code == 200
    assert r.json() == puppy2

def test_token_add_puppy():
    r = client.post("/kennels/4/puppies/new")
    assert r.status_code == 401
    assert r.is_client_error

def test_fields_add_puppy():
    r = client.post("/kennels/4/puppies/new", headers=admin_auth_header)
    assert r.status_code == 422
    assert r.is_client_error
    assert r.text == puppy_body_missing_error_text


def test_add_puppy():
    r = client.post("/kennels/4/puppies/new", headers=admin_auth_header, data=add_puppy_json, files=puppy_images)
    assert r.status_code == 200
    assert r.json()['breed'] == add_puppy_json['breed']
    assert r.json()['price'] == add_puppy_json['price']



admin_auth_header = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYXJjZWxvQGVtYWlsLmNvbSIsImV4cCI6MTcwMzQ1MTc2NH0.7H0tsroOtGhRmoixujPCqOb5w7fIB8YjTRkEnN88XCI"
}

add_breed_data = {"name": 'test_{0}'.format(random_string_gen())}

some_available_breeds = [
        {"name": "Pug", "id": 1},
        {"name": "Labrador", "id": 2},
        {"name": "Teeste", "id": 3},
        {"name": "LULUZI", "id": 4},
        {"name": "LULUZ2I", "id": 5},
        {"name": "Lulu da pom", "id": 6},
    ]

some_gallery_data = [{"id": 11}, {"id": 15}, {"id": 20}]

puppy2 = {
        "breed": "Pug",
        "microchip": False,
        "minimum_age_departure_in_days": 60,
        "price": 3000,
        "gender": -1,
        "birth": "2023-11-02T18:25:43.511000",
        "vermifuges": [
            {"brand": "ENDAL® PLUS - MSD", "date": "2023-11-22T18:25:43.511000"}
        ],
        "vaccines": [
            {"brand": "Bio Max", "type": "V8", "date": "2023-11-23T18:25:43.511000"}
        ],
        # "medias": [],
        "id": 2,
    }

kennel7 = {
        "name": "Canil Geize",
        "phone": "2233299833245199",
        "instagram": "22dreamp3u2pp23.com.br",
        "city": {"name": "Vitória da Conquista", "uf": "BA"},
        "address": "Avenida Olivia Flores",
        "cep": "39890000",
        "id": 7,
    }

puppies_from_kennel4 = [
        {
            "breed": 1,
            "microchip": False,
            "minimum_age_departure_in_days": 60,
            "price": 3000,
            "gender": -1,
            "birth": "2023-11-02T18:25:43.511000",
            "vermifuges": [
                {
                    "brand": "ENDAL® PLUS - MSD",
                    "date": "2023-11-22T18:25:43.511000",
                }
            ],
            "vaccines": [
                {
                    "brand": "Bio Max",
                    "type": "V8",
                    "date": "2023-11-23T18:25:43.511000",
                }
            ],
            "id": 29,
        },
        {
            "breed": 1,
            "microchip": True,
            "minimum_age_departure_in_days": 60,
            "price": 1990,
            "gender": 1,
            "birth": "2023-11-02T18:25:43.511000",
            "vermifuges": [
                {
                    "brand": "ENDAL® PLUS - MSD",
                    "date": "2023-11-22T18:25:43.511000",
                }
            ],
            "vaccines": [
                {
                    "brand": "Bio Max",
                    "type": "V8",
                    "date": "2023-11-23T18:25:43.511000",
                }
            ],
            "id": 30,
        },
        {
            "breed": 1,
            "microchip": True,
            "minimum_age_departure_in_days": 60,
            "price": 1990,
            "gender": 1,
            "birth": "2023-11-02T18:25:43.511000",
            "vermifuges": [
                {
                    "brand": "ENDAL® PLUS - MSD",
                    "date": "2023-11-22T18:25:43.511000",
                }
            ],
            "vaccines": [
                {
                    "brand": "Bio Max",
                    "type": "V8",
                    "date": "2023-11-23T18:25:43.511000",
                }
            ],
            "id": 31,
        },
        {
            "breed": 1,
            "microchip": True,
            "minimum_age_departure_in_days": 60,
            "price": 970,
            "gender": -1,
            "birth": "2023-11-02T18:25:43.511000",
            "vermifuges": [
                {
                    "brand": "HBO",
                    "date": "2023-11-22T18:25:43.511000",
                }
            ],
            "vaccines": [
                {
                    "brand": "Bio Max",
                    "type": "V8",
                    "date": "2023-11-23T18:25:43.511000",
                }
            ],
            "id": 37,
        },
    ]



puppy_body_missing_error_text = '{"detail":[{"type":"missing","loc":["body","breed"],"msg":"Field required","input":null,"url":"https://errors.pydantic.dev/2.3/v/missing"},{"type":"missing","loc":["body","microchip"],"msg":"Field required","input":null,"url":"https://errors.pydantic.dev/2.3/v/missing"},{"type":"missing","loc":["body","price"],"msg":"Field required","input":null,"url":"https://errors.pydantic.dev/2.3/v/missing"},{"type":"missing","loc":["body","gender"],"msg":"Field required","input":null,"url":"https://errors.pydantic.dev/2.3/v/missing"},{"type":"missing","loc":["body","birth"],"msg":"Field required","input":null,"url":"https://errors.pydantic.dev/2.3/v/missing"},{"type":"missing","loc":["body","vermifuges"],"msg":"Field required","input":null,"url":"https://errors.pydantic.dev/2.3/v/missing"},{"type":"missing","loc":["body","vaccines"],"msg":"Field required","input":null,"url":"https://errors.pydantic.dev/2.3/v/missing"},{"type":"missing","loc":["body","images"],"msg":"Field required","input":null,"url":"https://errors.pydantic.dev/2.3/v/missing"}]}'

add_puppy_json = {"breed": 4,
	"price": 970,
	"gender": -1,
	"birth": "2023-11-02T18:25:43.511000",
	"microchip": True,
	"minimum_age_departure_in_days": 60,
	"vermifuges": json.dumps([
		{
			"brand": "HBO",
			"date": "2023-11-22T18:25:43.511000"
		}
	]),
	"vaccines": json.dumps([
		{
			"brand": "Bio Max",
			"type": "V8",
			"date": "2023-11-23T18:25:43.511000"
		}
	])}

files = [f for f in os.listdir("./imgs")]
puppy_images = {
    "cover": files[0],
    "images": files[0]}