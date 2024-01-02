from . import test_main as main
import pytest


def test_fill_gallery():
    pytest.skip()
    response = main.client.get("/gallery")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()


some_gallery_data = [
    {
        "id": 116,
        "url": "https://devapigallery.blob.core.windows.net/bbac8099910041cfa3cd8f9f869d25f3/546877e157a44b4d9f8728f20bc0183c.jpeg",
    },
    {
        "id": 115,
        "url": "https://devapigallery.blob.core.windows.net/d6f1bd49a1a0465baf2c7144d2cf879f/6cb0c9536c214d59a0bc19be43dd3f04.jpeg",
    },
    {
        "id": 111,
        "url": "https://devapigallery.blob.core.windows.net/501bfec674294a549c8c8f94b246a401/640f219c24104dfaa60066d5b487e386.jpeg",
    },
]
