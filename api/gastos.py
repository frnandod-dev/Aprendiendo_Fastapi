from fastapi import APIRouter
from models.database import SessionLocal
from models.models import Gastos
from pydantic import BaseModel
from fastapi import HTTPException, Depends
from datetime import date
from api.usuarios import obtener_usuario_actual
from core.gasto import Gasto

class GastoSchema(BaseModel):
    nombre: str
    cantidad: float
    categoria: str
    fecha: date

router = APIRouter()

@router.get("/gastos")
def obtener_gastos(usuario: str = Depends(obtener_usuario_actual)):
    db = SessionLocal()
    gastos_todos = db.query(Gastos).all()
    db.close()
    return gastos_todos

@router.get(("/gasto/{id}"))
def obtener_gastos_id(id: int, usuario: str = Depends(obtener_usuario_actual)):
    db = SessionLocal()
    buscar_id = db.query(Gastos).filter(Gastos.id == id).first()
    db.close()
    if not buscar_id:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return buscar_id

@router.post("/gastos")
def crear_gasto(gasto : GastoSchema,usuario: str = Depends(obtener_usuario_actual)):
    if gasto.categoria not in Gasto.CATEGORIAS_VALIDAS:
        raise HTTPException(status_code= 422, detail="Categoria invalida")
    else:
        db = SessionLocal()
        nuevo_gasto = Gastos(nombre=gasto.nombre, cantidad=gasto.cantidad, categoria=gasto.categoria, fecha=gasto.fecha)
        validar_gasto = db.query(Gastos).filter(Gastos.nombre == gasto.nombre, Gastos.cantidad == gasto.cantidad).first()
        if not validar_gasto:
            try:
                db.add(nuevo_gasto)
                db.commit()
                db.close()
                return nuevo_gasto
            except Exception as e :
                db.rollback()
                db.close()
                raise HTTPException(status_code=500, detail="Error al guardar el gasto")
        else: 
            raise HTTPException(status_code=409, detail="Gasto repetido")
    

@router.put("/gasto/{id}")
def modificar_gasto(id: int, gasto: GastoSchema, usuario: str = Depends(obtener_usuario_actual)):
    if gasto.categoria not in Gasto.CATEGORIAS_VALIDAS:
        raise HTTPException(status_code=422, detail= " Categoria invalida")
    else:
        db = SessionLocal()
        validar_gastos = db.query(Gastos).filter(Gastos.nombre == gasto.nombre, Gastos.cantidad == gasto.cantidad, Gastos.id != id).first()
        if not validar_gastos:   
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
        else:
            raise HTTPException(status_code=409, detail="Gasto duplicado")   
     
@router.delete("/gasto/{id}")
def delete_gasto(id: int, usuario: str = Depends(obtener_usuario_actual)):
    db = SessionLocal()
    buscar_id_y_eliminar = db.query(Gastos).filter(Gastos.id == id).first()
    if buscar_id_y_eliminar:
        db.delete(buscar_id_y_eliminar)
        db.commit()
        db.close()
    else:
        raise HTTPException(status_code=404, detail="Gasto no encontrado")
    return {"mensaje": "Gasto eliminado"}

    
    