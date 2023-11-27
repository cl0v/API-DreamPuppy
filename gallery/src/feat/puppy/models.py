from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from gallery.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class PuppyModel(Base):
    __tablename__ = "puppies"

    id = Column(Integer, primary_key=True, nullable=False)
    breed = Column(Integer, ForeignKey("breeds.id"), nullable=False)
    price = Column(Integer, nullable=False)
    minimum_age_departure_in_days = Column(Integer, default=60, nullable=False)
    microchip = Column(Boolean, default=False, nullable=False)

    vermifuges = relationship("Vermifuge", back_populates="pet", uselist=True)
    vaccines = relationship("Vaccine", back_populates="pet", uselist=True)

    # cover_img = Column(String, nullable=True)
    # pictures = relationship("Media", back_populates="medias", uselist=True)


# Lista de vacinas
## Leitura: https://www.petlove.com.br/dicas/vacinas-de-cachorro
class Vaccine(Base):
    __tablename__ = "vaccines"

    id = Column(Integer, primary_key=True, nullable=False)
    puppy = Column(Integer, ForeignKey("puppies.id"), nullable=False)
    brand = Column(
        String, nullable=True
    )  # (Exemplo pra V8): Recombitek® C6/CV da Merial, Vanguard® HTLP 5/CV-L da Pfizer, Quantum® Dog DA2PPvL CV da Intervet Shering plough e Canigen® CH(A2) ppi/LCv da Virbac.
    type = Column(String, nullable=True)  # V6, V8, V10...
    date = Column(DateTime, nullable=True)

    pet = relationship("PuppyModel", back_populates="vaccines")


# Lista de vermifugos
class Vermifuge(Base):
    __tablename__ = "vermifuges"

    id = Column(Integer, primary_key=True, nullable=False)
    puppy = Column(Integer, ForeignKey("puppies.id"), nullable=False)
    brand = Column(String, nullable=True)  #
    date = Column(DateTime, nullable=True)

    pet = relationship("PuppyModel", back_populates="vermifuges")


# Qualquer tipo de mídia [publica] que envolve os filhotes (.jpg, .png, .mp4, .mp3, .gif)
# class Media(Base):
#     __tablename__ = "medias"

#     id = Column(Integer, primary_key=True, nullable=False)
#     url = Column(String, unique=True)
#     puppy = Column(Integer, ForeignKey("puppies.id"), nullable=False)
#     uploaded_at = Column(DateTime, nullable=False, default=func.now())

#     pet = relationship("PuppyModel", back_populates="pictures")

class BreedModel(Base):
    __tablename__ = "breeds"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, index=True, unique=True)
