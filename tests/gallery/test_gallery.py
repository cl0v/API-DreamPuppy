from .. import test_app
import unittest


class GalleryProperlyFunction(unittest.TestCase):
    def test_fill_gallery(self):
        response = test_app.client.get("/gallery/?size=24&page=1")
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertIsInstance(response.json()["items"], list)


if __name__ == "__main__":
    unittest.main()
