from . import test_main as main


def test_fill_gallery():
    response = main.client.get("/gallery/?size=3&page=1")
    assert response.status_code == 200
    assert response.json()
    print(response.json())
    assert isinstance(response.json(), dict)
    assert isinstance(response.json()['items'], list)

