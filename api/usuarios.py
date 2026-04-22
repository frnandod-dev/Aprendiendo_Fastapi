from fastapi import APIRouter
from models.database import SessionLocal
from models.models import Usuario
from pydantic import BaseModel
from fastapi import HTTPException, Depends
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


SECRET_KEY = "mi_clave_secreta"
AlGORITHM = "HS256" 
pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")
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
def login_usuario(from_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    validar_nombre_u = db.query(Usuario).filter(Usuario.nombre_usuario == from_data.username).first()
    if validar_nombre_u:
        password_verify = pwd_context.verify(from_data.password, validar_nombre_u.password)        
        if password_verify:
           payload = {
               "sub": validar_nombre_u.nombre_usuario,
               "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
               }
           token = jwt.encode(payload, SECRET_KEY, algorithm=AlGORITHM)
           return {"access_token": token, "token_type": "bearer"}
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
   

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    try:
        decode_usuario = jwt.decode(token,SECRET_KEY,algorithms=[AlGORITHM])
        usuario = decode_usuario["sub"]
        return usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalido o expirado")
    