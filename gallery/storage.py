import os
from azure.storage.blob import BlobServiceClient, PublicAccess, ContentSettings, BlobClient
import uuid
from gallery.env import AZURE_STORAGE_CNN_STR

storage_connection_string = AZURE_STORAGE_CNN_STR

blob_service_client = BlobServiceClient.from_connection_string(
    storage_connection_string
)

def create_container(uuid: str):
    return blob_service_client.create_container(uuid, public_access=PublicAccess.BLOB.value,)

def create_blob(uuid: str, container_uuid: str, content_type:str='image/jpeg')-> BlobClient:
    content_type = content_type.split('/')[-1]
    return blob_service_client.get_blob_client(
        container=container_uuid, blob=f"{uuid}.{content_type}"
    )

def upload_blob(blob: BlobClient, data, content_type:str='image/jpeg'):
    return blob.upload_blob(data, content_type=content_type)