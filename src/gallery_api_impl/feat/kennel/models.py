from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Sequence,
    Numeric,
)  # , Boolean,
from sqlalchemy.orm import relationship
from gallery_api_impl.database import Base
from sqlalchemy.sql import func


class KennelModel(Base):
    __tablename__ = "kennels"

    id = Column(
        Integer,
        Sequence("kennels_id_seq"),
        primary_key=True,
        autoincrement=True,
    )
    name = Column(
        String,
        nullable=False,
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
    )
    phone = Column(
        String,
        nullable=False,
    )
    instagram = Column(
        String,
        nullable=True,
    )
    address = Column(
        String,
        nullable=False,
    )
    city = Column(
        String,
        nullable=False,
    )
    uf = Column(
        String,
        nullable=False,
    )
    cep = Column(
        String,
        nullable=False,
    )

    lat = Column(
        Numeric,
        nullable=False,
        index=True,
    )
    lon = Column(
        Numeric,
        nullable=False,
        index=True,
    )
