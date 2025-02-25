# schemas/categoria.py
from pydantic import BaseModel

class CategoriaBase(BaseModel):
    nombre: str
    icono: str | None = None  # Opcional
    descripcion: str | None = None  # Opcional

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id: int

    class Config:
        from_attributes = True