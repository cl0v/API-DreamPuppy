from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from gallery.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)

    credentials = relationship("UserCredentials", back_populates="user", uselist=False)


class UserCredentials(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    pwd = Column(String)
    # sub="$email $cred_id $user_id" Separar por espaco pode ajudar muito
    jwt = Column(String, unique=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Verificar necessidade de ser nulo

    user = relationship("User", back_populates="credentials")
