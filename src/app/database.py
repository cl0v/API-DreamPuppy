import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base
from app.env import POSTGRES_URL


# SQLALCHEMY_DATABASE_URL = sa.engine.URL.create(
#     drivername="postgresql",
#     database=POSTGRES_DATABASE_NAME,ƒ
#     username=POSTGRES_USER,
#     password=POSTGRES_PASSWORD,
#     host=POSTGRES_SERVER,
#     port=POSTGRES_PORT,
# )


engine = sa.create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
