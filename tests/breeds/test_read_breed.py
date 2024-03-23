from ..test_app import client
import unittest


class TestDefaultBreedReadingBehavior(unittest.TestCase):
    def test_read_breed_list(self):
        r = client.get("/breeds/list")
        
        self.assertEqual(r.status_code, 200)
        self.assertIsInstance(r.json(), list)
