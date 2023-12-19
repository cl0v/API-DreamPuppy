# TODO: Remover


import boto3

from . import exceptions
from fastapi import UploadFile

client = boto3.client("s3")
bucket = "viana.dev2.gallery"


def get_url_by_key(puppy_uuid: str, media_uuid: str):
    key = "{0}/{1}".format(puppy_uuid, media_uuid)
    url = client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=3600,
    )
    return url


def upload_img(puppy_uuid: str, media_uuid: str, media: UploadFile):
    if media.content_type == "application/octet-stream":
        raise exceptions.PuppyStorageException(status_code=500, message="Erro ao salvar imagem")
    key = "{0}/{1}".format(puppy_uuid, media_uuid)
    client.upload_fileobj(
        media.file,
        bucket,
        key,
        ExtraArgs={
            "ContentType": media.content_type,
            "ACL": "public-read",
        },
    )
