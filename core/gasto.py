class Gasto:
    CATEGORIAS_VALIDAS = ["fijo", "variable"]
    def __init__(self, nombre, cantidad, categoria, fecha):
        self.nombre = nombre
        self.cantidad = cantidad
        self.categoria = categoria
        self.fecha = fecha
        if not isinstance(self.nombre, str):
            raise ValueError("Nombre debe ser valido")
        if self.cantidad <= 0:
            raise ValueError("Cantidad debe ser mayor a 0")
        if self.categoria not in self.CATEGORIAS_VALIDAS:
            raise ValueError("Categoria debe ser fijo o variable")
        

        
