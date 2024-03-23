import unittest
import json
from .values import breed_json, expected_response_json, new_random_breed_json
from ..test_app import client, admin_auth_header



class TestDefaultBreedCreatingBehavior(unittest.TestCase):
    def test_check_duplicate_breed(self):
        r = client.post(
            "/breeds/new",
            content=json.dumps(breed_json),
            headers=admin_auth_header,
        )

        self.assertEqual(r.status_code, 409)
        self.assertEqual(r.json(), expected_response_json)

    def test_add_new_breed(self):
        r = client.post(
            "/breeds/new",
            content=json.dumps(new_random_breed_json),
            headers=admin_auth_header,
        )

        self.assertEqual(r.status_code, 200)
        self.assertIsNotNone(r.json())
