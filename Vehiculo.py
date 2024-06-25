
class Vehiculo:
    def __init__(self, id, orientacion, longitud, fila, col):
        self.id = id
        self.orientacion = orientacion
        self.longitud = longitud
        self.fila = fila
        self.col = col

    def get_positions(self):
        """Devuelve una lista de todas las posiciones ocupadas por el vehículo."""
        posiciones = []
        if self.orientacion == 'H':
            for i in range(self.longitud):
                posiciones.append((self.fila, self.col + i))
        else:  # orientacion == 'V'
            for i in range(self.longitud):
                posiciones.append((self.fila + i, self.col))
        return posiciones
