# models/categoria.py
from sqlalchemy import Column, Integer, String
from database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    icono = Column(String(255), nullable=True)  # Puede ser una URL o nombre de archivo
    descripcion = Column(String(500), nullable=True)  # Texto descriptivo