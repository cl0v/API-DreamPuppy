from ..test_app import client, admin_auth_header
from .. import utils
import json

kid = 100


def test_err_token_add_kennel():
    r = client.post("/kennels/new")
    assert r.is_client_error
    assert r.status_code == 401


def test_err_content_add_kennel():
    r = client.post(
        "/kennels/new",
        headers=admin_auth_header,
    )
    assert r.is_client_error
    assert r.status_code == 422


def test_add_n_read_kennel():
    r = client.post(
        "/kennels/new",
        headers=admin_auth_header,
        content=json.dumps(kennel0),
    )

    d = r.json()
    kid = d["id"]

    assert r.status_code == 200
    assert kid > 0

    r2 = client.get(f"kennels/{kid}")
    d2 = r2.json()

    assert r2.status_code == 200
    assert d2["id"] == kid
    d2.pop("geo")

    for k in d2.keys():
        if k not in kennel0.keys():
            continue
        inval = kennel0[k]
        outval = d2[k]
        assert inval == outval


def test_err_duplicate_add_kennel():
    r = client.post(
        "/kennels/new",
        headers=admin_auth_header,
        content=json.dumps(kennel0),
    )
    assert r.status_code == 409
    assert r.json() == {"msg": "Esse telefone já foi cadastrado, tente outro."}


def test_token_list_puppies_from_kennel():
    r = client.get("/kennels/4/puppies/")
    assert r.status_code == 401
    assert r.is_client_error


def test_get_kennel():
    r = client.get(f"/kennels/{kid}")
    assert r.status_code == 200


def test_list_puppies_from_kennel():
    r = client.get("/kennels/4/puppies/", headers=admin_auth_header)
    assert r.status_code == 200


kennel0 = {
    "name": "Canil Geize",
    "phone": utils.random_string_gen(9),
    "instagram": utils.random_string_gen(12),
    "city": "Vitória da Conquista",
    "uf": "BA",
    "address": "Avenida Olivia Flores",
    "cep": "39890000",
    "geo": {"lat": 1.2332321, "lon": 4.23321},
}
