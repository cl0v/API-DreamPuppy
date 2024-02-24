from sqlalchemy import Column, ForeignKey, Integer, String, DateTime,  Sequence #, Boolean,
from app.database import Base
from sqlalchemy.sql import func


class KennelModel(Base):
    __tablename__ = "kennels"

    id = Column(Integer,Sequence('kennel_id_seq', start=11), primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    phone = Column(String, nullable=False)
    instagram = Column(String, nullable=True)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False, index=True)
    uf = Column(String, nullable=False, index=True)
    cep = Column(String, nullable=False)


class KennelsNPuppies(Base):
    __tablename__ = "kennels_n_puppies"

    kennel_id = Column(Integer, ForeignKey("kennels.id"), nullable=False)
    puppy_id = Column(
        Integer, ForeignKey("puppies.id"), nullable=False, unique=True, primary_key=True
    )
