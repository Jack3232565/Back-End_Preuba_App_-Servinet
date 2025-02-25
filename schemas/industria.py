# schemas/industria.py
from pydantic import BaseModel

class IndustriaBase(BaseModel):
    nombre: str
    icono: str | None = None  # Opcional
    descripcion: str | None = None  # Opcional

class IndustriaCreate(IndustriaBase):
    pass

class IndustriaResponse(IndustriaBase):
    id: int

    class Config:
        from_attributes = True