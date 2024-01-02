import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base
from app.env import (
    POSTGRES_PASSWORD,
    POSTGRES_USER,
    POSTGRES_DATABASE_NAME,
    POSTGRES_SERVER,
)

SQLALCHEMY_DATABASE_URL = sa.engine.URL.create(
    drivername="postgresql",
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_SERVER,
    database=POSTGRES_DATABASE_NAME,
)

engine = sa.create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
