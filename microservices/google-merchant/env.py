import os
from dotenv import load_dotenv

load_dotenv()

MERCHANT_ID : str | None = os.getenv("MERCHANT_ID")
