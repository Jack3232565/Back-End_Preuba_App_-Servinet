# models/datos_personales.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base
from datetime import datetime

class DatosPersonales(Base):
    __tablename__ = "datos_personales"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, unique=True)
    titulo = Column(String(50), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=True)
    email = Column(String(100), nullable=False)
    rfc = Column(String(13), nullable=False)
    genero = Column(String(10), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    industria_id = Column(Integer, ForeignKey("industrias.id"), nullable=False)
    direccion = Column(String(255), nullable=False)
    estado = Column(String(100), nullable=False)
    cp = Column(String(10), nullable=False)
    telefono = Column(String(20), nullable=False)
    fotografia = Column(String(255), nullable=True)