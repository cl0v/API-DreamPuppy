import os
from dotenv import load_dotenv

load_dotenv()


TEST_NAME: str | None = os.getenv("TEST_NAME")
API_VERSION: str | None = os.getenv("API_VERSION")

ADMIN_JWT:  str | None = os.getenv("ADMIN_JWT")

POSTGRES_URL:  str | None = os.getenv("POSTGRES_URL")

cloudflare_account_id:  str | None = os.getenv("CFI_ID")
cloudflare_token:  str | None = os.getenv("CFI_TOKEN")

# POSTGRES_USER:  str | None = os.getenv("POSTGRES_USER")
# POSTGRES_PASSWORD:  str | None = os.getenv("POSTGRES_PASSWORD")
# POSTGRES_DATABASE_NAME:  str | None = os.getenv("POSTGRES_DATABASE_NAME")
# POSTGRES_SERVER:  str | None = os.getenv("POSTGRES_SERVER")
# POSTGRES_PORT:  str | None = os.getenv("POSTGRES_PORT")

AZURE_STORAGE_CNN_STR:  str | None = os.getenv("AZURE_STORAGE_CNN_STR")
AZURE_STORAGE_NAME:  str | None = os.getenv("AZURE_STORAGE_NAME")
AZURE_STORAGE_KEY:  str | None = os.getenv("AZURE_STORAGE_KEY")
