from starlette.testclient import TestClient
from main import app
import pytest

client = TestClient(app)


def test_fill_gallery():
    response = client.get("/gallery")
    assert response.status_code == 200
    for a in [{"id": 11}, {"id": 15}, {"id": 20}]:
        assert a in response.json()


def test_list_breeds():
    r = client.get("/breeds/list")
    assert r.status_code == 200
    for a in [
        {"name": "Pug", "id": 1},
        {"name": "Labrador", "id": 2},
        {"name": "Teeste", "id": 3},
        {"name": "LULUZI", "id": 4},
        {"name": "LULUZ2I", "id": 5},
        {"name": "Lulu da pom", "id": 6},
    ]:
        assert a in r.json()


def test_get_kennel():
    r = client.get("/kennels/7")
    assert r.status_code == 200
    assert r.json() == {
        "name": "Canil Geize",
        "phone": "2233299833245199",
        "instagram": "22dreamp3u2pp23.com.br",
        "city": {"name": "Vitória da Conquista", "uf": "BA"},
        "address": "Avenida Olivia Flores",
        "cep": "39890000",
        "id": 7,
    }


def test_unauth_list_puppies_from_kennel():
    r = client.get("/kennels/4/puppies/")
    assert r.status_code == 401


def test_list_puppies_from_kennel():
    r = client.get(
        "/kennels/4/puppies/",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYXJjZWxvQGVtYWlsLmNvbSIsImV4cCI6MTcwMzQ1MTc2NH0.7H0tsroOtGhRmoixujPCqOb5w7fIB8YjTRkEnN88XCI"
        },
    )
    assert r.status_code == 200
    for v in [
        {
            "breed": 1,
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
                {"brand": "ENDAL® PLUS - MSD", "date": "2023-11-22T18:25:43.511000"}
            ],
            "vaccines": [
                {"brand": "Bio Max", "type": "V8", "date": "2023-11-23T18:25:43.511000"}
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
                {"brand": "ENDAL® PLUS - MSD", "date": "2023-11-22T18:25:43.511000"}
            ],
            "vaccines": [
                {"brand": "Bio Max", "type": "V8", "date": "2023-11-23T18:25:43.511000"}
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
            "vermifuges": [{"brand": "HBO", "date": "2023-11-22T18:25:43.511000"}],
            "vaccines": [
                {"brand": "Bio Max", "type": "V8", "date": "2023-11-23T18:25:43.511000"}
            ],
            "id": 37,
        },
    ]:
        assert v in r.json()


def test_empty_list_puppies_from_kennel():
    r = client.get(
        "/kennels/2/puppies/",
        headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYXJjZWxvQGVtYWlsLmNvbSIsImV4cCI6MTcwMzQ1MTc2NH0.7H0tsroOtGhRmoixujPCqOb5w7fIB8YjTRkEnN88XCI"
        },
    )
    assert r.status_code == 200
    assert r.json() == []


def test_get_puppy_from_id():
    pytest.skip()
    r = client.get("/puppies/2")
    assert r.status_code == 200
    assert r.json() == {
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
        "medias": [],
        "id": 2,
    }
