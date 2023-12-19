from azure.storage.blob import (
    BlobServiceClient,
    PublicAccess,
)

from fastapi import UploadFile
import os
from app.feat.puppy.exceptions import PuppyStorageException

blob_service_client = BlobServiceClient.from_connection_string(
    os.environ["AZURE_STORAGE_CNN_STR"]
)


def get_url_by_key(puppy_uuid: str, media_uuid: str):
    return blob_service_client.get_blob_client(puppy_uuid, media_uuid).primary_endpoint


def create_container(puppy_uuid: str):
    blob_service_client.create_container(
        puppy_uuid,
        public_access=PublicAccess.BLOB.value,
    )


def upload_img(puppy_uuid: str, media_uuid: str, media: UploadFile):
    if media.content_type == "application/octet-stream":
        raise PuppyStorageException(status_code=500, message="Erro ao salvar imagem")
    blob = blob_service_client.get_blob_client(container=puppy_uuid, blob=media_uuid)
    blob.upload_blob(media.file, content_type=media.content_type)
