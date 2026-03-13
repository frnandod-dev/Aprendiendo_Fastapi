from fastapi import FastAPI
from api.gastos import router as gastos_router

app = FastAPI()

app.include_router(gastos_router)

