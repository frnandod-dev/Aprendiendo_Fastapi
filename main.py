from fastapi import FastAPI
from api.gastos import router as gastos_router
from api.ingresos import router as ingresos_router
from api.usuarios import router as usuarios_router
app = FastAPI()
@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido al controlador de Gastos e ingresos"}

app.include_router(gastos_router)
app.include_router(ingresos_router)
app.include_router(usuarios_router)

