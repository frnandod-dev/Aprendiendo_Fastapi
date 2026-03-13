from core.ingreso import Ingreso
import pytest
from datetime import date
fecha = date(2026, 3, 10)

@pytest.fixture
def ingreso():
    return Ingreso(2800, "empleo", fecha)

def test_cantidad_valida(ingreso):
    assert ingreso.cantidad > 0

def test_origen_valido(ingreso):
    assert ingreso.origen == "empleo"

def test_cantidad_invalida():
    with pytest.raises(ValueError):
        Ingreso(-56, "empleo", fecha)

def test_origen_invalido():
    with pytest.raises(ValueError):
        Ingreso(1564, 45, fecha)



