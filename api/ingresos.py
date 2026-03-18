from fastapi import APIRouter
from models.database import SessionLocal
from models.models import Ingresos
from pydantic import BaseModel
from fastapi import HTTPException
from datetime import date

class IngresoSchema(BaseModel):
    cantidad: int
    origen: str
    fecha: date

router = APIRouter()

@router.get("/ingresos")
def obtener_ingresos():
    db = SessionLocal()
    ingresos_todos = db.query(Ingresos).all()
    db.close()
    return ingresos_todos

@router.get("/ingresos/{id}")
def obtener_ingresos_id(id: int):
    db = SessionLocal()
    buscar_ingreso = db.query(Ingresos).filter(Ingresos.id == id).first()
    db.close()
    if not buscar_ingreso:
        raise HTTPException(status_code=404, detail="Ingreso no encontrado")
    return buscar_ingreso


@router.post("/ingresos")
def agregar_ingreso(ingreso: IngresoSchema):
    db = SessionLocal()
    nuevo_ingreso = Ingresos(cantidad=ingreso.cantidad, origen=ingreso.origen, fecha=ingreso.fecha)
    try:
        db.add(nuevo_ingreso)
        db.commit()
        db.close()
        return nuevo_ingreso
    except Exception as e:
        db.rollback()
        db.close()
        raise HTTPException(status_code=500, detail="Error al guardar Ingreso")

@router.put("/ingresos/{id}")
def modificar_ingreso(id: int, ingreso: IngresoSchema):
    db = SessionLocal()
    buscar_id_ingresos = db.query(Ingresos).filter(Ingresos.id == id).first()
    if buscar_id_ingresos:
        buscar_id_ingresos.cantidad = ingreso.cantidad
        buscar_id_ingresos.origen = ingreso.origen
        buscar_id_ingresos.fecha = ingreso.fecha
        db.commit()
        db.close()
        return buscar_id_ingresos
    else:
        raise HTTPException(status_code=404, detail="Ingreso no encontrado")

@router.delete("/ingresos/{id}")
def eliminar_ingreso(id: int):
    db = SessionLocal()
    buscar_id = db.query(Ingresos).filter(Ingresos.id == id).first()
    if buscar_id:
        db.delete(buscar_id)
        db.commit()
        db.close()
    else:
        raise HTTPException(status_code=404, detail="Ingreso no encontrado")
    return {"mensaje": "Ingreso eliminado"}
    