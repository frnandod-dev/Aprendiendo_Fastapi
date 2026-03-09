class Ingreso:
    def __init__(self, cantidad, origen, fecha):
        self.cantidad = cantidad
        self.origen = origen
        self.fecha = fecha
        if self.cantidad <= 0:
            raise ValueError("Cantidad debe ser mayor a 0")
        if not isinstance(self.origen, str):
            raise ValueError("Origen debe ser Valido")
        