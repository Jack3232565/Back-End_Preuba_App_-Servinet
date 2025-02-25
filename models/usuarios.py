# models/usuario.py
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from database import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)  # Añadido unique=True
    email = Column(String(100), nullable=False, unique=True)  # Ya tenía unique=True
    contraseña = Column(String(255), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('nombre', name='uq_nombre'),  # Constraint explícita para nombre
        UniqueConstraint('email', name='uq_email'),    # Constraint explícita para email
    )