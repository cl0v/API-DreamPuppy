from . import test_main as main
import pytest
import json
from . import utils


def test_get_kennel():
    r = main.client.get("/kennels/7")
    assert r.status_code == 200
    assert r.json() == kennel7


def test_err_token_add_kennel():
    r = main.client.post("/kennels/new")
    assert r.is_client_error
    assert r.status_code == 401


def test_err_content_add_kennel():
    r = main.client.post(
        "/kennels/new",
        headers=main.admin_auth_header,
    )
    assert r.is_client_error
    assert r.status_code == 422


def test_add_kennel():
    r = main.client.post(
        "/kennels/new",
        headers=main.admin_auth_header,
        content=json.dumps(kennel0),
    )
    assert r.status_code == 200
    assert r.json()["id"] > 0


def test_err_duplicate_add_kennel():
    pytest.skip()
    r = main.client.post(
        "/kennels/new",
        headers=main.admin_auth_header,
        content=json.dumps(kennel0),
    )
    assert r.status_code == 409


def test_token_list_puppies_from_kennel():
    r = main.client.get("/kennels/4/puppies/")
    assert r.status_code == 401
    assert r.is_client_error


def test_list_puppies_from_kennel():
    r = main.client.get("/kennels/4/puppies/", headers=main.admin_auth_header)
    assert r.status_code == 200
    for v in puppies_from_kennel4:
        assert v in r.json()


def test_empty_list_puppies_from_kennel():
    r = main.client.get("/kennels/2/puppies/", headers=main.admin_auth_header)
    assert r.status_code == 200
    assert r.json() == []


kennel0 = {
    "name": "Canil Geize",
    "phone": utils.random_string_gen(9),
    "instagram": utils.random_string_gen(12),
    "city": "Vitória da Conquista",
    "uf": "BA",
    "address": "Avenida Olivia Flores",
    "cep": "39890000",
}

kennel7 = {
    "name": "Canil Geize",
    "phone": "ssss",
    "instagram": "ssss.com.br",
    "city": "Vitória da Conquista",
    "uf": "BA",
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
        "pedigree": False,
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
        "pedigree": False,
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
        "pedigree": False,
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
        "pedigree": False,
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
