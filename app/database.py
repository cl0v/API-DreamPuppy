from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.env import (
    POSTGRES_PASSWORD,
    POSTGRES_USER,
    POSTGRES_DATABASE_NAME,
    POSTGRES_SERVER,
)


SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
