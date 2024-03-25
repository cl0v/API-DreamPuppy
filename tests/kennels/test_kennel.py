from ..test_app import client, admin_auth_header
from . import values
import json
from gallery_api_impl.constants.strings import (
    DUPLICATED_PHONE_ERROR,
    DUPLICATED_INSTAGRAM_ERROR,
    DUPLICATED_KENNEL_ERROR,
    EMPTY_PHONE_ERROR,
)
import unittest

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
        content=json.dumps(values.kennel0),
    )

    d = r.json()
    kid = d["id"]

    assert r.status_code == 200
    assert kid > 0

    r2 = client.get(f"kennels/{kid}")
    d2 = r2.json()

    assert r2.status_code == 200
    assert d2["id"] == kid

    for k in d2.keys():
        if k not in values.kennel0.keys():
            continue
        inval = values.kennel0[k]
        outval = d2[k]
        assert inval == outval


def test_err_duplicate_add_kennel():
    r = client.post(
        "/kennels/new",
        headers=admin_auth_header,
        content=json.dumps(values.kennel0),
    )
    assert r.status_code == 409
    assert r.json() == {"msg": DUPLICATED_PHONE_ERROR}


def test_token_list_puppies_from_kennel():
    r = client.get("/kennels/4/puppies/")
    assert r.status_code == 401
    assert r.is_client_error


def test_get_kennel():
    r = client.get(f"/kennels/{kid}")
    assert r.status_code == 200


class TestDefaultKennelAPI(unittest.TestCase):

    def test_list_puppies_from_kennel(self):
        r = client.get("/kennels/4/puppies/", headers=admin_auth_header)
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)
