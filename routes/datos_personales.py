# routes/datos_personales.py
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from config import app
from models.datos_personales import DatosPersonales
from models.categorias import Categoria
from models.industria import Industria
from schemas.datos_personales import DatosPersonalesCreate, DatosPersonalesResponse
from database import get_db
from routes.auth import get_current_user
from models.usuarios import Usuario
from datetime import datetime

# Crear datos personales
@app.post("/datos-personales/", response_model=DatosPersonalesResponse, tags=["Datos Personales"], summary="Crear datos personales")
def crear_datos_personales(
    datos: DatosPersonalesCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if db.query(Categoria).filter(Categoria.id == datos.categoria_id).first() is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if db.query(Industria).filter(Industria.id == datos.industria_id).first() is None:
        raise HTTPException(status_code=404, detail="Industria no encontrada")
    if db.query(DatosPersonales).filter(DatosPersonales.usuario_id == usuario.id).first():
        raise HTTPException(status_code=400, detail="Datos personales ya registrados para este usuario")
    
    fecha_nacimiento = datetime.strptime(datos.fecha_nacimiento, "%d/%m/%Y").date()
    db_datos = DatosPersonales(
        usuario_id=usuario.id,
        titulo=datos.titulo,
        nombre=datos.nombre,
        apellido_paterno=datos.apellido_paterno,
        apellido_materno=datos.apellido_materno,
        email=usuario.email,
        rfc=datos.rfc,
        genero=datos.genero,
        fecha_nacimiento=fecha_nacimiento,
        categoria_id=datos.categoria_id,
        industria_id=datos.industria_id,
        direccion=datos.direccion,
        estado=datos.estado,
        cp=datos.cp,
        telefono=datos.telefono,
        fotografia=datos.fotografia
    )
    db.add(db_datos)
    db.commit()
    db.refresh(db_datos)
    return db_datos

# Leer datos personales
@app.get("/datos-personales/", response_model=DatosPersonalesResponse, tags=["Datos Personales"], summary="Obtener mis datos personales")
def obtener_datos_personales(usuario: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    datos = db.query(DatosPersonales).filter(DatosPersonales.usuario_id == usuario.id).first()
    if datos is None:
        raise HTTPException(status_code=404, detail="Datos personales no encontrados")
    return datos

# Actualizar datos personales
@app.put("/datos-personales/", response_model=DatosPersonalesResponse, tags=["Datos Personales"], summary="Actualizar mis datos personales")
def actualizar_datos_personales(
    datos: DatosPersonalesCreate,
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_datos = db.query(DatosPersonales).filter(DatosPersonales.usuario_id == usuario.id).first()
    if db_datos is None:
        raise HTTPException(status_code=404, detail="Datos personales no encontrados")
    if db.query(Categoria).filter(Categoria.id == datos.categoria_id).first() is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if db.query(Industria).filter(Industria.id == datos.industria_id).first() is None:
        raise HTTPException(status_code=404, detail="Industria no encontrada")
    
    fecha_nacimiento = datetime.strptime(datos.fecha_nacimiento, "%d/%m/%Y").date()
    for key, value in datos.dict().items():
        if key == "fecha_nacimiento":
            setattr(db_datos, key, fecha_nacimiento)
        else:
            setattr(db_datos, key, value)
    db_datos.email = usuario.email  # Mantener el email del usuario autenticado
    db.commit()
    db.refresh(db_datos)
    return db_datos

# Eliminar datos personales
@app.delete("/datos-personales/", tags=["Datos Personales"], summary="Eliminar mis datos personales")
def eliminar_datos_personales(usuario: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    db_datos = db.query(DatosPersonales).filter(DatosPersonales.usuario_id == usuario.id).first()
    if db_datos is None:
        raise HTTPException(status_code=404, detail="Datos personales no encontrados")
    db.delete(db_datos)
    db.commit()
    return {"detail": "Datos personales eliminados"}