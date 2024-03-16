from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    credentials = relationship("UserCredentials", back_populates="user", uselist=False)


class UserCredentials(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True)  # nullable?
    pwd = Column(String)  # nullable?
    jwt = Column(String, unique=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, default=None)

    user = relationship("User", back_populates="credentials", uselist=False)