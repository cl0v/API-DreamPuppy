import os
from dotenv import load_dotenv

load_dotenv()

MERCHANT_JWT : str | None = os.getenv("MERCHANT_JWT")
MERCHANT_ID : str | None = os.getenv("MERCHANT_ID")
