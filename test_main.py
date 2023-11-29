from starlette.testclient import TestClient
from gallery.main import app

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

def 