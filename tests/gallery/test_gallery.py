from .. import test_app
import unittest

# from json import encoder


class GalleryProperlyFunction(unittest.TestCase):
    def test_fill_gallery(self):
        response = test_app.client.get("/gallery/?size=24&page=1")
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())
        self.assertIsInstance(response.json(), dict)
        self.assertIsInstance(response.json()["items"], list)
        self.assertLessEqual(response.json()["items"].__len__(), 24)
        

    # Testa a funcionalidade de proximidade garantindo que filhotes que estão cadastrados
    # Nos canis com latitude e longitude mais proximas apareçam em ordem
    # # # # 
    # Ordem de proximidade começa por p176 > p177 > p178 sendo 178 o mais distante
    def test_prio_proximity(self):
        response = test_app.client.get(
            "/gallery/?size=24&page=1",
            headers={
                "lat": str(
                    -14.8719219,
                ).encode("utf-8"),
                "lon": str(
                    -40.8185112,
                ).encode("utf-8"),
            },
        )
        self.assertEqual(response.status_code, 200)

        js = response.json()
        self.assertIsNotNone(js)
        self.assertIsInstance(js, dict)

        li: list = js["items"]
        self.assertIsInstance(li, list)
        p176 = next(x for x in li if x["id"] == 176)
        p177 = next(x for x in li if x["id"] == 177)
        p178 = next(x for x in li if x["id"] == 178)

        # Menor o index, mais perto da localização solicitada
        # Como os filhotes foram cadastrados em ordem contraria, sem a geoloc apareceria ao contrario
        self.assertLess(li.index(p176), li.index(p177))
        self.assertLess(li.index(p176), li.index(p178))
        self.assertLess(li.index(p177), li.index(p178))


    # Quando não informado nenhuma localização a ordem fica normal
    # com base em quando foi adicionado o filhote
    def test_prio_proximity_off(self):
        response = test_app.client.get("/gallery/?size=24&page=1")
        self.assertEqual(response.status_code, 200)

        js = response.json()
        self.assertIsNotNone(js)
        self.assertIsInstance(js, dict)

        li: list = js["items"]
        self.assertIsInstance(li, list)
        
        p176 = next(x for x in li if x["id"] == 176)
        p177 = next(x for x in li if x["id"] == 177)
        p178 = next(x for x in li if x["id"] == 178)

        # Menor o index, mais perto da localização solicitada
        # Como os filhotes foram cadastrados em ordem contraria, sem a geoloc apareceria ao contrario
        self.assertGreater(li.index(p176), li.index(p177))
        self.assertGreater(li.index(p176), li.index(p178))
        self.assertGreater(li.index(p177), li.index(p178))


if __name__ == "__main__":
    unittest.main()
