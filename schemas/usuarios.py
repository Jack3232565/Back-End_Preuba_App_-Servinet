# schemas/usuario.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    contraseña: str

class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: str
    fecha_registro: datetime

    class Config:
        from_attributes = True

class UsuarioUpdatePassword(BaseModel):
    contraseña_actual: str
    contraseña_nueva: str

class UsuarioRecoverPassword(BaseModel):  # Ajustado: solo email
    email: EmailStr
    contraseña_nueva: str