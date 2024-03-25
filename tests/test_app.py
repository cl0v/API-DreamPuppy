from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from gallery_api_impl.database import Base, get_db
from gallery_api_impl.env import POSTGRES_URL
from gallery_api_impl.main import app


SQLALCHEMY_DATABASE_URL = POSTGRES_URL


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)



admin_auth_header = {"Authorization": "Bearer 0"}

