from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from gallery.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Puppy(Base):
    __tablename__ = "puppies"

    id = Column(Integer, primary_key=True, nullable=False)
    breed = Column(Integer, ForeignKey("breeds.id"), nullable=False)
    microchip = Column(Integer, ForeignKey("microschips.id"), nullable=True)
    minimum_age_departure_in_days = Column(Integer, default=60, nullable=False)

    cover_img = Column(String, nullable=False)

    pictures = relationship("Media", back_populates="medias", uselist=True)
    vaccines = relationship("Vaccine", back_populates="vaccines", uselist=True)
    vermifuges = relationship("Vermifuge", back_populates="vermifuges", uselist=True)


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


# Lista de vermifugos
class Vermifuge(Base):
    __tablename__ = "vermifuges"

    id = Column(Integer, primary_key=True, nullable=False)
    puppy = Column(Integer, ForeignKey("puppies.id"), nullable=False)
    brand = Column(String, nullable=True)  #
    date = Column(DateTime, nullable=True)


# O unico microchip que o cachorro pode ter
class Microchip(Base):
    __tablename__ = "microschips"

    id = Column(Integer, primary_key=True, nullable=False)
    brand = Column(String, nullable=True)


# Qualquer tipo de mídia [publica] que envolve os filhotes (.jpg, .png, .mp4, .mp3, .gif)
class Media(Base):
    __tablename__ = "medias"

    id = Column(Integer, primary_key=True, nullable=False)
    url = Column(String, unique=True)  # nullable?
    puppy = Column(Integer, ForeignKey("puppies.id"), nullable=False)
    uploaded_at = Column(DateTime, nullable=False, default=func.now())


class Breed(Base):
    __tablename__ = "breeds"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, index=True)
