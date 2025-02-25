# routes/usuario.py
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from config import app, pwd_context
from models.usuarios import Usuario
from schemas.usuarios import (
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdatePassword,
    UsuarioRecoverPassword
)
from database import get_db

@app.get("/", tags=["General"])
def read_root():
    return {"message": "Bienvenido a la API de Servinet"}

@app.post("/usuarios/", response_model=UsuarioResponse, tags=["Usuarios"], summary="Crear un nuevo usuario")
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if db.query(Usuario).filter(Usuario.nombre == usuario.nombre).first():
        raise HTTPException(status_code=400, detail="Usuario existente (nombre ya registrado)")
    if db.query(Usuario).filter(Usuario.email == usuario.email).first():
        raise HTTPException(status_code=400, detail="Usuario existente (email ya registrado)")
    
    contraseña_cifrada = pwd_context.hash(usuario.contraseña)
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        email=usuario.email,
        contraseña=contraseña_cifrada
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@app.get("/usuarios/{usuario_id}", response_model=UsuarioResponse, tags=["Usuarios"], summary="Obtener un usuario por ID")
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.put("/usuarios/{usuario_id}/contraseña", response_model=UsuarioResponse, tags=["Usuarios"], summary="Actualizar contraseña de un usuario")
def actualizar_contraseña(
    usuario_id: int,
    datos: UsuarioUpdatePassword,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not pwd_context.verify(datos.contraseña_actual, usuario.contraseña):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
    
    usuario.contraseña = pwd_context.hash(datos.contraseña_nueva)
    db.commit()
    db.refresh(usuario)
    return usuario

@app.post("/usuarios/recuperar-contraseña", response_model=UsuarioResponse, tags=["Usuarios"], summary="Recuperar contraseña por email")
def recuperar_contraseña(
    datos: UsuarioRecoverPassword,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.email == datos.email).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Correo no encontrado")
    
    usuario.contraseña = pwd_context.hash(datos.contraseña_nueva)
    db.commit()
    db.refresh(usuario)
    return usuario