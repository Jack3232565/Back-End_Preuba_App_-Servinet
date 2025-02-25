# config.py
from fastapi import FastAPI
from passlib.context import CryptContext
from database import engine, Base
import models.usuarios  # Importa el módulo, no el nombre
import models.categorias
import models.industria
import models.datos_personales

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Servinet API",
    description="API para gestionar usuarios, categorías, industrias y datos personales",
    version="1.0.0"
)