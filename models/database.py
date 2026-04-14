from sqlalchemy import create_engine
from models.models import Base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///gastos_ingresos.db")
SessionLocal = sessionmaker(bind=engine)
