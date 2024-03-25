from .. import test_app as main
from .. import utils
from . import values
import json
from gallery_api_impl.constants.strings import DUPLICATED_BREED_ERROR
import unittest



class TestDefaultPuppiesBehavior(unittest.TestCase):
    def test_add_breed(self):
        r = main.client.post(
            "/breeds/new",
            content=json.dumps(values.add_breed_data),
            headers=main.admin_auth_header,
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual( r.json()["name"], values.add_breed_data["name"])
        self.assertGreaterEqual(r.json()["id"], 0)

    def test_err_token_add_breed(self):
        r = main.client.post("/breeds/new", data=values.add_breed_data)
        assert r.status_code == 401
        assert r.is_client_error

    def test_err_duplicate_add_breed(self):
        r = main.client.post(
            "/breeds/new",
            content=json.dumps(values.add_breed_data),
            headers=main.admin_auth_header,
        )
        assert r.status_code == 409
        assert r.json()["msg"] == DUPLICATED_BREED_ERROR
        assert r.is_client_error

    def test_list_breeds(self):
        r = main.client.get("/breeds/list")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_get_puppy_from_id(self):
        r = main.client.get("/puppies/2")
        assert r.status_code == 200
        assert r.json()

    def test_err_token_add_puppy(self):
        r = main.client.post(f"/kennels/{values.ace_kennel_id}/puppies/new")
        assert r.status_code == 401
        assert r.is_client_error

    def test_err_fields_add_puppy(self):
        r = main.client.post(
            f"/kennels/{values.ace_kennel_id}/puppies/new", headers=main.admin_auth_header
        )
        assert r.status_code == 422
        assert r.is_client_error

    def test_add_n_read_puppy(self):
        pid = add_puppy()

        r2 = read_puppy(pid)

        d2 = r2.json()
        assert isinstance(values.add_puppy_json["breed"], int)
        assert isinstance(d2["breed"], str)
        d2.pop("breed")

        # assert "images" in d2.keys()
        # assert isinstance(d2["images"], list)
        # assert len(d2["images"]) == 1
        assert d2["id"] == pid

def add_puppy():
    r = main.client.post(
        f"/kennels/{values.ace_kennel_id}/puppies/new",
        headers=main.admin_auth_header,
        content=json.dumps(values.add_puppy_json),
    )
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
