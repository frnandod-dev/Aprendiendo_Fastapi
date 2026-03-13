from core.gasto import Gasto
import pytest 
from datetime import date

fecha = date(2026, 3, 9)
@pytest.fixture
def gasto():
    return Gasto("Despensa", 1346, "variable", fecha)

def test_gasto_nombre_correcto(gasto):
    assert gasto.nombre == "Despensa"

def test_cantidad_adecuada(gasto):
    assert gasto.cantidad > 0

def test_categoria_valida(gasto):
    assert gasto.categoria in Gasto.CATEGORIAS_VALIDAS

def test_cantidad_invalida():
    with pytest.raises(ValueError):
        Gasto("Despensa", -20, "variable", fecha)

def test_nombre_invalido():
    with pytest.raises(ValueError):
        Gasto(34, 1234, "variable", fecha)

def test_categoria_invalida():
    with pytest.raises(ValueError):
        Gasto("Despensa", 1234, "indefinido", fecha)



