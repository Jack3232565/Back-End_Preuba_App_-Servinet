# models/industria.py
from sqlalchemy import Column, Integer, String
from database import Base

class Industria(Base):
    __tablename__ = "industrias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    icono = Column(String(255), nullable=True)  # Puede ser una URL o nombre de archivo
    descripcion = Column(String(500), nullable=True)  # Texto descriptivo