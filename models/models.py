from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Gastos(Base):
    __tablename__ = "gastos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    cantidad = Column(Float)
    categoria = Column(String)
    fecha = Column(Date)


class Ingresos(Base):
    __tablename__ = "ingresos"
    id = Column(Integer, primary_key=True)
    cantidad = Column(Float)
    origen = Column(String)
    fecha = Column(Date)
    

