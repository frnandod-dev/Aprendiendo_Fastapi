# Sistema de Gestion de Gastos e Ingresos 
Gestiona los Gastos y los Ingresos permitiendo registrar, guardar, modificar y eliminar.

Establece ingresos por origen, cantidad y fecha.
Establece gastos por nombre, cantidad, categoria y fecha. 

Validaciones y captura de errores en POST y PUT en los CRUD de ingresos y gastos.

- python 3.14.0
- FastAPI 0.135.1
- pydantic 2.12.5
- SQLAlchemy 2.0.48
- uvicorn 0.41.0
- pytest 9.0.2

## Installation
### 1. Clona el repositorio
```
git clone git@github.com:frnandod-dev/Aprendiendo_Fastapi.git
```
### 2. Crear el entorno virtual
```
python -m venv venv 
```
### 3. Activar el entorno virtual 
```
source venv/Scripts/activate
```
### 4. Instalar dependencias 
```
pip install -r requirements.txt
```
### 5. Arrancar API
```
uvicorn main:app --reload
```

## Usage
### FastAPI genera documentacion interactiva automaticamente en: 
```
http://127.0.0.1:8000/docs#/
```

### Seperado por los recursos Ingresos y Gastos: 
- GET /gasto
- GET /gasto/{id}
- POST /gastos
- PUT /gasto/{id}
- DELETE /gasto/{id}

- GET /ingresos
- GET /ingresos/{id}
- POST /ingresos
- PUT /ingresos/{id}
- DELETE /ingresos/{id}