from starlette.testclient import TestClient
from gallery.app import app


client = TestClient(app)

admin_auth_header = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtYXJjZWxvQGVtYWlsLmNvbSIsImV4cCI6MTcwMzQ1MTc2NH0.7H0tsroOtGhRmoixujPCqOb5w7fIB8YjTRkEnN88XCI"
}

