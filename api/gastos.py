from fastapi import APIRouter
from models.database import SessionLocal
from models.models import Gastos
from pydantic import BaseModel
from fastapi import HTTPException

router = APIRouter()

@router.get("/")
def inicio():
    return {"mensaje": "Bienvenidos al controlador de Gastos"}

@router.get("/gastos")
def obtener_gastos():
    db = SessionLocal()
    gastos_todos = db.query(Gastos).all()
    db.close()
    return gastos_todos