import requests
from app.env import cloudflare_account_id, cloudflare_token
from fastapi import UploadFile


def upload_image(image: UploadFile, puppy_uuid: str) -> str:
    upload_url = f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_account_id}/images/v1"
    # TODO: Mudar o nome para que seja condizente com o id do filhote
    image.filename = puppy_uuid

    response = (
        requests.post(
            upload_url,
            files={
                # 'metadata': {"puppy_id": puppy_uuid},
                "file": image.file,
            },
            headers={
                "Authorization": f"Bearer {cloudflare_token}",
            },
        ),
    )

    img_id = response[0].json()["result"]["id"]
    return img_id


def get_image_public_url(image_id: str) -> str:
    get_url = f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_account_id}/images/v1/{image_id}"
    response = requests.get(
        get_url,
        headers={
            "Authorization": f"Bearer {cloudflare_token}",
        },
    )
    img_url = response.json()["result"]["variants"][0]
    return img_url
