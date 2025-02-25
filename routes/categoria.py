# routes/categoria.py
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from config import app
from models.categorias import Categoria
from schemas.categoria import CategoriaCreate, CategoriaResponse
from database import get_db

@app.post("/categorias/", response_model=CategoriaResponse, tags=["Categorías"], summary="Crear una nueva categoría")
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    if db.query(Categoria).filter(Categoria.nombre == categoria.nombre).first():
        raise HTTPException(status_code=400, detail="Categoría ya existe")
    db_categoria = Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@app.get("/categorias/", response_model=list[CategoriaResponse], tags=["Categorías"], summary="Listar todas las categorías")
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()

@app.get("/categorias/{categoria_id}", response_model=CategoriaResponse, tags=["Categorías"], summary="Obtener una categoría por ID")
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@app.put("/categorias/{categoria_id}", response_model=CategoriaResponse, tags=["Categorías"], summary="Actualizar una categoría")
def actualizar_categoria(categoria_id: int, categoria: CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if db.query(Categoria).filter(Categoria.nombre == categoria.nombre, Categoria.id != categoria_id).first():
        raise HTTPException(status_code=400, detail="Nombre de categoría ya existe")
    for key, value in categoria.dict().items():
        setattr(db_categoria, key, value)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@app.delete("/categorias/{categoria_id}", tags=["Categorías"], summary="Eliminar una categoría")
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    db_categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(db_categoria)
    db.commit()
    return {"detail": "Categoría eliminada"}