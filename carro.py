import os
import pygetwindow as gw
from tablero import TABLERO
class carro:
    def __init__(self, tablero):
        self.tablero = tablero
        self.tablero.dimensionarTablero()
        self.tablero.dibujarTablero()
        self.vehiculo_jugador = self.tablero.vehiculo_jugador

        if not self.vehiculo_jugador:
            raise ValueError("No se encontró el vehículo del jugador (A) en el tablero.")

    def moverIzquierda(self, vehiculoMover):
        vehiculo = self.buscar_vehiculo(vehiculoMover)
        nueva_posicion = {'fila': vehiculo['posicion']['fila'], 'columna': vehiculo['posicion']['columna'] - 1}
        if vehiculo['orientacion'] == 'horizontal' and self._es_posicion_valida(nueva_posicion) or vehiculo['caracter'] =='A':
            self.tablero.actualizarVehiculo(vehiculoMover, nueva_posicion)
            vehiculo['posicion'] = nueva_posicion
            self.tablero.dibujarTablero()
        else:
            print("Movimiento no válido")

    def moverDerecha(self, vehiculoMover):
        vehiculo = self.buscar_vehiculo(vehiculoMover)
        nueva_posicion = {'fila': vehiculo['posicion']['fila'], 'columna': vehiculo['posicion']['columna'] + 1}
        if vehiculo['orientacion'] == 'horizontal' and self._es_posicion_valida(nueva_posicion):
            self.tablero.actualizarVehiculo(vehiculoMover, nueva_posicion)
            vehiculo['posicion'] = nueva_posicion
            self.tablero.dibujarTablero()
        else:
            print("Movimiento no válido")

    def moverArriba(self, vehiculoMover):
        vehiculo = self.buscar_vehiculo(vehiculoMover)
        nueva_posicion = {'fila': vehiculo['posicion']['fila'] - 1, 'columna': vehiculo['posicion']['columna']}
        if vehiculo['orientacion'] == 'vertical' and self._es_posicion_valida(nueva_posicion):
            self.tablero.actualizarVehiculo(vehiculoMover, nueva_posicion)
            vehiculo['posicion'] = nueva_posicion
            self.tablero.dibujarTablero()
        else:
            print("Movimiento no válido")

    def moverAbajo(self, vehiculoMover):
        vehiculo = self.buscar_vehiculo(vehiculoMover)
        nueva_posicion = {'fila': vehiculo['posicion']['fila'] + 1, 'columna': vehiculo['posicion']['columna']}
        if vehiculo['orientacion'] == 'vertical' and self._es_posicion_valida(nueva_posicion):
            self.tablero.actualizarVehiculo(vehiculoMover, nueva_posicion)
            vehiculo['posicion'] = nueva_posicion
            self.tablero.dibujarTablero()
        else:
            print("Movimiento no válido")

    def buscar_vehiculo(self, vehiculoMover):
        for vehiculo in self.tablero.vehiculos:
            if vehiculo['caracter'] == vehiculoMover:
                return vehiculo
        raise ValueError(f"No se encontró el vehículo '{vehiculoMover}' en el tablero.")

    def _es_posicion_valida(self, posicion):
        fila, columna = posicion['fila'], posicion['columna']
        if 1 <= columna <= self.tablero.columnas and 1 <= fila <= self.tablero.filas:
            for obstaculo in self.tablero.obstaculos:
                if obstaculo['posicion'] == posicion:
                    return False
            return True
        return False


if __name__ == "__main__":
    tablero = TABLERO()
    jugador = carro(tablero)

    print(f"Vehículo del jugador (A) en: {jugador.vehiculo_jugador}")
    print("Obstáculos inamovibles (B) en:")
    for obstaculo in tablero.obstaculos:
        print(obstaculo)
    print("Otros vehículos en:")
    for vehiculo in tablero.vehiculos:
        print(vehiculo)

    jugador.moverDerecha("G") #! Hay un problema, el ptro caracter se borró, xd
