import os
import pygetwindow as gw

class TABLERO:
    def __init__(self, nombre_txt="controlador.txt"):
        self.tablero = []
        self.vehiculo_jugador = None
        self.meta = None
        self.obstaculos = []
        self.vehiculos = []
        self.paredes = []
        self.filas = 0
        self.columnas = 0
        self.nombreTxt = nombre_txt

    def dimensionarTablero(self):
        with open(self.nombreTxt, 'r') as archivo:
            for fila, linea in enumerate(archivo):
                linea = linea.strip()
                if len(linea) > self.columnas:
                    self.columnas = len(linea)
                fila_tablero = []

                for columna, caracter in enumerate(linea):
                    posicion = {'fila': fila + 1, 'columna': columna + 1}
                    fila_tablero.append(caracter)
                    if caracter == 'A':
                        self.vehiculo_jugador = posicion
                        self.vehiculos.append({'tipo': 'vehiculo', 'caracter': 'A', 'posicion': posicion, 'orientacion': None})
                    elif caracter == '0':
                        self.meta = posicion
                    elif caracter == 'B':
                        self.obstaculos.append({'tipo': 'obstaculo', 'posicion': posicion})
                    elif caracter == '#':
                        self.paredes.append({'tipo': 'pared', 'posicion': posicion})
                    elif caracter.isalpha() and (caracter.islower() or (caracter.isupper() and caracter not in {'A', 'B'})):
                        self.vehiculos.append({'tipo': 'vehiculo', 'caracter': caracter, 'posicion': posicion, 'orientacion': None})
                self.tablero.append(fila_tablero)
                self.filas = fila + 1
        self.actualizarOrientacionVehiculos()

    def actualizarOrientacionVehiculos(self):
        for vehiculo in self.vehiculos:
            fila, columna = vehiculo['posicion']['fila'], vehiculo['posicion']['columna']
            caracter = vehiculo['caracter']
            if columna < self.columnas and self.tablero[fila - 1][columna] == caracter:
                vehiculo['orientacion'] = 'horizontal'
            elif fila < self.filas and self.tablero[fila][columna - 1] == caracter:
                vehiculo['orientacion'] = 'vertical'
            elif columna > 1 and self.tablero[fila - 1][columna - 2] == caracter:
                vehiculo['orientacion'] = 'horizontal'
            elif fila > 1 and self.tablero[fila - 2][columna - 1] == caracter:
                vehiculo['orientacion'] = 'vertical'

    def getInfo(self):
        return self.vehiculo_jugador, self.meta, self.obstaculos, self.paredes, self.vehiculos, self.filas, self.columnas

    def actualizarVehiculo(self, vehiculo, nueva_posicion):
        # Verifica si la nueva posición es una pared u otro obstáculo
        for pared in self.paredes:
            if pared['posicion'] == nueva_posicion:
                print("Movimiento inválido: hay una pared en la nueva posición.")
                return False  # Movimiento inválido

        for obstaculo in self.obstaculos:
            if obstaculo['posicion'] == nueva_posicion:
                print("Movimiento inválido: hay un obstáculo en la nueva posición.")
                return False  # Movimiento inválido

        for v in self.vehiculos:
            if v['posicion'] == nueva_posicion:
                print("Movimiento inválido: hay otro vehículo en la nueva posición.")
                return False  # Movimiento inválido

        posicion_anterior = None
        if vehiculo == 'A':
            posicion_anterior = self.vehiculo_jugador
            self.vehiculo_jugador = nueva_posicion
        else:
            for v in self.vehiculos:
                if v['caracter'] == vehiculo:
                    posicion_anterior = v['posicion']
                    v['posicion'] = nueva_posicion
                    break

        if posicion_anterior:
            self.tablero[posicion_anterior['fila'] - 1][posicion_anterior['columna'] - 1] = '.'
        self.tablero[nueva_posicion['fila'] - 1][nueva_posicion['columna'] - 1] = vehiculo
        return True  # Movimiento válido

    def dibujarTablero(self):
        self.cls()
        print("   ", end=" ")
        for col in range(1, self.columnas + 1):
            print(f"{col:2}   ", end=" ")
        print()

        for fila_num, fila in enumerate(self.tablero, start=1):
            print(f"{fila_num:2}    ", end="")
            for item in fila:
                print(f"{item:2}    ", end="")
            print()
            print()
            print()

    def cls(self):
        if os.name == 'nt':
            os.system('cls')

# Ejemplo de uso
tablero = TABLERO("controlador.txt")
tablero.dimensionarTablero()
tablero.dibujarTablero()

# Intentar mover el vehículo 'A' a una nueva posición (ejemplo)
nueva_posicion = {'fila': 2, 'columna': 3}
if tablero.actualizarVehiculo('A', nueva_posicion):
    print("Movimiento realizado con éxito.")
else:
    print("Movimiento no permitido.")
tablero.dibujarTablero()
