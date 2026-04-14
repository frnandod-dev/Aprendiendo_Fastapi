from fastapi import APIRouter
from models.database import SessionLocal
from models.models import Usuario
from pydantic import BaseModel
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "mi_clave_secreta"
AlGORITHM = "HS256" 
pwd_context = CryptContext(schemes=["bcrypt"])

class UsuarioSchema(BaseModel):
    nombre: str
    nombre_usuario: str
    password: str

class UsuarioShemaOut(BaseModel):
    id: int
    nombre: str
    nombre_usuario: str 
    model_config = {"from_attributes": True}

class UsuarioShemaLogin(BaseModel):
    nombre_usuario: str
    password: str

router = APIRouter()

@router.post("/usuarios/login")
def login_usuario(usuario: UsuarioShemaLogin):
    db = SessionLocal()
    validar_nombre_u = db.query(Usuario).filter(Usuario.nombre_usuario == usuario.nombre_usuario).first()
    if validar_nombre_u:
        password_verify = pwd_context.verify(usuario.password, validar_nombre_u.password)        
        if password_verify:
           payload = {
               "sub": validar_nombre_u.nombre_usuario,
               "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
               }
           
           token = jwt.encode(payload, SECRET_KEY, algorithm=AlGORITHM)
           return token 
        else:
            raise HTTPException(status_code=401, detail = "Usuario o contraseña incorrecta")
    else:
        raise HTTPException(status_code=401, detail="Contaseña o Usuario incorrecto")
            

@router.post("/usuarios/registro", response_model= UsuarioShemaOut)
def crear_usuario(usuario : UsuarioSchema):
    db = SessionLocal()
    validar_nombre_usuario = db.query(Usuario).filter(Usuario.nombre_usuario == usuario.nombre_usuario).first()
    if not validar_nombre_usuario:
        password_hash =  pwd_context.hash(usuario.password)
        nuevo_usuario = Usuario(nombre=usuario.nombre, nombre_usuario=usuario.nombre_usuario, password=password_hash)
        try:
            db.add(nuevo_usuario)
            db.commit()
            db.refresh(nuevo_usuario)
            db.close()
            return nuevo_usuario
        except Exception as e :
            db.rollback()
            db.close()
            raise HTTPException(status_code=500, detail="Error al guardar Usuario")
    else:
        raise HTTPException(status_code=409, detail="Nombre de Usuario ya utilizado")
   


