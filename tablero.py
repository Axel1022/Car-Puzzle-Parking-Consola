import os
import pygetwindow as gw

class TABLERO:
    def __init__(self, nombre_txt="./controlador.txt"):
        self.tablero = []
        self.vehiculo_jugador = None
        self.meta = None
        self.obstaculos = []
        self.vehiculos = []
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

                #! Por si no entiende:
                """
                    Aqui aparte del cometido de la funcion, se le agrega : 'orientacion': None
                    Eso es porque o para, xd
                    en el txt no se coloca explicitamente la orientacion y pues mas abajo hay una funcion que ferifica si
                    el carro esta en vertical u horizontal... Abajo ta como funciona
                """
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
                    elif caracter.isalpha() and (caracter.islower() or (caracter.isupper() and caracter not in {'A', 'B'})):
                        self.vehiculos.append({'tipo': 'vehiculo', 'caracter': caracter, 'posicion': posicion, 'orientacion': None})
                self.tablero.append(fila_tablero)
                self.filas = fila + 1
        self.actualizarOrientacionVehiculos()

    def actualizarOrientacionVehiculos(self):
        #! Finciona tan que así:
        """
           El verifica su arededor, si el carro tiene arriba... un caracter igual al que tiene,
           pues se determina si esta horizontal o vertical

           Se entendió?
        """
        for vehiculo in self.vehiculos:
            fila, columna = vehiculo['posicion']['fila'], vehiculo['posicion']['columna']
            caracter = vehiculo['caracter']
            # Revisar atras y alante
            if columna < self.columnas and self.tablero[fila - 1][columna] == caracter:
                vehiculo['orientacion'] = 'horizontal'
            # Revisar arriba y abajo
            elif fila < self.filas and self.tablero[fila][columna - 1] == caracter:
                vehiculo['orientacion'] = 'vertical'
            # Revisar atras
            elif columna > 1 and self.tablero[fila - 1][columna - 2] == caracter:
                vehiculo['orientacion'] = 'horizontal'
            # Revisar arriba
            elif fila > 1 and self.tablero[fila - 2][columna - 1] == caracter:
                vehiculo['orientacion'] = 'vertical'
        print( vehiculo['orientacion'])

    def getInfo(self):
        return self.vehiculo_jugador, self.meta, self.obstaculos, self.vehiculos, self.filas, self.columnas

    def actualizarVehiculo(self, vehiculo, nueva_posicion):
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

    def dibujarTablero(self):
        #! Peligro!!
        #!No cambien nada aquí
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
