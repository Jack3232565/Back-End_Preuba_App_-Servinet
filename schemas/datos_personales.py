# schemas/datos_personales.py
from pydantic import BaseModel, EmailStr, validator, Field
from datetime import date, datetime

class DatosPersonalesBase(BaseModel):
    titulo: str
    nombre: str
    apellido_paterno: str
    apellido_materno: str | None = None
    rfc: str
    genero: str
    fecha_nacimiento: str  # Formato "DD/MM/YYYY" para entrada
    categoria_id: int
    industria_id: int
    direccion: str
    estado: str
    cp: str
    telefono: str
    fotografia: str | None = None

class DatosPersonalesCreate(DatosPersonalesBase):
    @validator("fecha_nacimiento")
    def validate_fecha_nacimiento(cls, value):
        try:
            fecha = datetime.strptime(value, "%d/%m/%Y").date()
        except ValueError:
            raise ValueError("Formato de fecha debe ser DD/MM/YYYY")
        hoy = date(2025, 2, 25)  # Fecha actual del sistema
        edad = hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
        if edad < 18:
            raise ValueError("El usuario debe tener al menos 18 años")
        return value

    @validator("genero")
    def validate_genero(cls, value):
        validos = ["femenino", "masculino", "n/b"]
        if value not in validos:
            raise ValueError("Género debe ser 'femenino', 'masculino' o 'n/b'")
        return value

class DatosPersonalesResponse(BaseModel):
    id: int
    titulo: str
    nombre: str
    apellido_paterno: str
    apellido_materno: str | None = None
    email: EmailStr
    rfc: str
    genero: str
    fecha_nacimiento: str = Field(..., description="Fecha en formato DD/MM/YYYY")
    categoria_id: int
    industria_id: int
    direccion: str
    estado: str
    cp: str
    telefono: str
    fotografia: str | None = None

    @validator("fecha_nacimiento", pre=True)
    def format_fecha_nacimiento(cls, value):
        if isinstance(value, date):
            return value.strftime("%d/%m/%Y")
        return value

    class Config:
        from_attributes = True