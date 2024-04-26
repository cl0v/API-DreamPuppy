import os
from dotenv import load_dotenv

load_dotenv()

API_VERSION: str | None = os.getenv("API_VERSION")

ADMIN_JWT:  str | None = os.getenv("ADMIN_JWT")

POSTGRES_URL:  str | None = os.getenv("POSTGRES_URL")

cloudflare_account_id:  str | None = os.getenv("CFI_ID")
cloudflare_token:  str | None = os.getenv("CFI_TOKEN")
