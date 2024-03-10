import requests
from app.env import cloudflare_account_id, cloudflare_token
from fastapi import UploadFile


def upload_image(image: UploadFile, puppy_uuid: str) -> str:
    upload_url = f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_account_id}/images/v1"

    response = (
        requests.post(
            upload_url,
            files={
                # 'metadata': puppy_uuid,
                "file": image.file
            },
            headers={
                "Authorization": f"Bearer {cloudflare_token}",
            },
        ),
    )

    img_id = response[0].json()["result"]["id"]
    imgs = response[0].json()["result"]["variants"]
    img_url = next(filter(contains_public_str, imgs), None)
    return img_id, img_url


# def get_image_public_url(image_id: str) -> str:
#     get_url = f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_account_id}/images/v1/{image_id}"
#     response = requests.get(
#         get_url,
#         headers={
#             "Authorization": f"Bearer {cloudflare_token}",
#         },
#     )
#     imgs: list[str] = response.json()["result"]["variants"]
#     img_url = next(filter(contains_public_str, imgs), None)
#     return img_url


def contains_public_str(val):
    return "public" in val


def get_gallery_image_url(image_id: str) -> str:
    get_url = f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_account_id}/images/v1/{image_id}"
    response = requests.get(
        get_url,
        headers={
            "Authorization": f"Bearer {cloudflare_token}",
        },
    )
    imgs: list[str] = response.json()["result"]["variants"]
    img_url = next(filter(contains_gallery_str, imgs), None)
    return img_url


def contains_gallery_str(val):
    return "gallerySmall" in val
