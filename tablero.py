
import os
import pygetwindow as gw

"""
    pip install pygetwindow

"""
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

    def abrirNotepad(self): # ! Importante
        archivo = r"controlador.txt"

        print("Abriendo archivo...")
        os.startfile(archivo)

        ventana_encontrada = False
        while not ventana_encontrada:
            windows = gw.getWindowsWithTitle("controlador.txt - ")
        print("Ventana abierta correctamente.")

        # TODO: Falta terminar aquí
        # ? La idea es que se abra el notepad automaticamente y detecte el momento en que este se cierra para continuar con el flujo...
        # ! Pero hay un problema... Intentalo...

    def dimensionarTablero(self):
        # ? Estoy manejando las posiciones iniciando en 1!! OJO AQUÍ
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
                    elif caracter == '0':
                        self.meta = posicion
                    elif caracter == 'B':
                        self.obstaculos.append({'tipo': 'obstaculo', 'posicion': posicion})
                    elif caracter.isalpha() and (caracter.islower() or (caracter.isupper() and caracter not in {'A', 'B'})):
                        self.vehiculos.append({'tipo': 'vehiculo', 'caracter': caracter, 'posicion': posicion})
                self.tablero.append(fila_tablero)
                self.filas = fila + 1

    def mostrar_info(self):
        print(f"Vehículo del jugador (A) en: {self.vehiculo_jugador}")
        print(f"Meta (0) en: {self.meta}")
        print("Obstáculos inamovibles (B) en:")
        for obstaculo in self.obstaculos:
            print(obstaculo)
        print("Otros vehículos en:")
        for vehiculo in self.vehiculos:
            print(vehiculo)
        print(f"Número de filas: {self.filas}")
        print(f"Número de columnas: {self.columnas}")

    def dibujarTablero(self):
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

tablero = TABLERO()
tablero.abrirNotepad()
