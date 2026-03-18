from fastapi import APIRouter
from models.database import SessionLocal
from models.models import Gastos
from pydantic import BaseModel
from fastapi import HTTPException
from datetime import date

class GastoSchema(BaseModel):
    nombre: str
    cantidad: float
    categoria: str
    fecha: date

router = APIRouter()

@router.get("/gastos")
def obtener_gastos():
    db = SessionLocal()
    gastos_todos = db.query(Gastos).all()
    db.close()
    return gastos_todos

@router.get(("/gasto/{id}"))
def obtener_gastos(id: int):
    db = SessionLocal()
    buscar_id = db.query(Gastos).filter(Gastos.id == id).first()
    db.close()
    if not buscar_id:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return buscar_id

@router.post("/gastos")
def crear_gasto(gasto : GastoSchema):
    db = SessionLocal()
    nuevo_gasto = Gastos(nombre=gasto.nombre, cantidad=gasto.cantidad, categoria=gasto.categoria, fecha=gasto.fecha)
    db.add(nuevo_gasto)
    db.commit()
    db.close()
    return nuevo_gasto

@router.put("/gasto/{id}")
def modificar_gasto(id: int, gasto: GastoSchema):
    db = SessionLocal()
    buscar_id = db.query(Gastos).filter(Gastos.id == id).first()
    if buscar_id:
        buscar_id.nombre = gasto.nombre
        buscar_id.cantidad = gasto.cantidad
        buscar_id.categoria = gasto.categoria
        buscar_id.fecha = gasto.fecha
        db.commit()
        db.close()
        return buscar_id
    else:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    
@router.delete("/gasto/{id}")
def delete_gasto(id: int):
    db = SessionLocal()
    buscar_id_y_eliminar = db.query(Gastos).filter(Gastos.id == id).first()
    if buscar_id_y_eliminar:
        db.delete(buscar_id_y_eliminar)
        db.commit()
        db.close()
    else:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return {"mensaje": "Gasto eliminado"}

    
    