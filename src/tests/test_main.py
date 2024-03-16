from starlette.testclient import TestClient
from app.main import app


client = TestClient(app)

admin_auth_header = {
    "Authorization": "Bearer 0"
}

