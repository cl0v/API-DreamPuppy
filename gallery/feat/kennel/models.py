from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from gallery.database import Base
from sqlalchemy.sql import func


class KennelModel(Base):
    __tablename__ = "kennels"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    phone = Column(String, nullable=False, unique=True)
    instagram = Column(String, nullable=True, unique=True)
    city = Column(Integer, ForeignKey("cities.id"), index=True, nullable=False)
    address = Column(String, nullable=False)
    cep = Column(String, nullable=False)


class CityModel(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    uf = Column(String, index=True, nullable=False)


class KennelsNPuppies(Base):
    __tablename__ = "kennels_n_puppies"

    kennel_id = Column(Integer, ForeignKey("kennels.id"), nullable=False)
    puppy_id = Column(Integer, ForeignKey("puppies.id"), nullable=False, unique=True, primary_key=True)
