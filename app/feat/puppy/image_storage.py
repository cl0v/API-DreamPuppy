import requests
from app.env import cloudflare_account_id, cloudflare_token
from fastapi import UploadFile


url = "https://jsonplaceholder.typicode.com/posts/1"
upload_url = (
    f"https://api.cloudflare.com/client/v4/accounts/${cloudflare_account_id}/images/v1"
)
list_url = (
    f"https://api.cloudflare.com/client/v4/accounts/${cloudflare_account_id}/images/v2"
)


def upload_image(image: UploadFile, puppy_uuid: str):
    private_img = False
    response = (
        requests.post(
            upload_url,
            files={
                # "metadata": {"puppy_id": puppy_uuid},
                "requireSignedURLs": private_img,
                "file": image.file,
            },
            headers={
                "Authorization": f"Bearer ${cloudflare_token}",
                "Content-Type": "application/json",
            },
        ),
    )
    # response_json = response.json()
    print(response)


response = requests.get(url)
