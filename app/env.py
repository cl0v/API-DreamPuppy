import os

TEST_NAME:str = os.getenv("TEST_NAME")

ADMIN_JWT:str = os.getenv("ADMIN_JWT")

POSTGRES_USER:str = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD:str = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DATABASE_NAME:str = os.getenv('POSTGRES_DATABASE_NAME')
POSTGRES_SERVER:str = os.getenv('POSTGRES_SERVER') # postgresserver

AZURE_STORAGE_CNN_STR:str = os.getenv("AZURE_STORAGE_CNN_STR")
