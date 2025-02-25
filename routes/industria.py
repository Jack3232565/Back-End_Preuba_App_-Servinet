# routes/industria.py
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from config import app
from models.industria import Industria
from schemas.industria import IndustriaCreate, IndustriaResponse
from database import get_db

@app.post("/industrias/", response_model=IndustriaResponse, tags=["Industrias"], summary="Crear una nueva industria")
def crear_industria(industria: IndustriaCreate, db: Session = Depends(get_db)):
    if db.query(Industria).filter(Industria.nombre == industria.nombre).first():
        raise HTTPException(status_code=400, detail="Industria ya existe")
    db_industria = Industria(**industria.dict())
    db.add(db_industria)
    db.commit()
    db.refresh(db_industria)
    return db_industria

@app.get("/industrias/", response_model=list[IndustriaResponse], tags=["Industrias"], summary="Listar todas las industrias")
def listar_industrias(db: Session = Depends(get_db)):
    return db.query(Industria).all()

@app.get("/industrias/{industria_id}", response_model=IndustriaResponse, tags=["Industrias"], summary="Obtener una industria por ID")
def obtener_industria(industria_id: int, db: Session = Depends(get_db)):
    industria = db.query(Industria).filter(Industria.id == industria_id).first()
    if industria is None:
        raise HTTPException(status_code=404, detail="Industria no encontrada")
    return industria

@app.put("/industrias/{industria_id}", response_model=IndustriaResponse, tags=["Industrias"], summary="Actualizar una industria")
def actualizar_industria(industria_id: int, industria: IndustriaCreate, db: Session = Depends(get_db)):
    db_industria = db.query(Industria).filter(Industria.id == industria_id).first()
    if db_industria is None:
        raise HTTPException(status_code=404, detail="Industria no encontrada")
    if db.query(Industria).filter(Industria.nombre == industria.nombre, Industria.id != industria_id).first():
        raise HTTPException(status_code=400, detail="Nombre de industria ya existe")
    for key, value in industria.dict().items():
        setattr(db_industria, key, value)
    db.commit()
    db.refresh(db_industria)
    return db_industria

@app.delete("/industrias/{industria_id}", tags=["Industrias"], summary="Eliminar una industria")
def eliminar_industria(industria_id: int, db: Session = Depends(get_db)):
    db_industria = db.query(Industria).filter(Industria.id == industria_id).first()
    if db_industria is None:
        raise HTTPException(status_code=404, detail="Industria no encontrada")
    db.delete(db_industria)
    db.commit()
    return {"detail": "Industria eliminada"}