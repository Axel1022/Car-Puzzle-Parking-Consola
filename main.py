from collections import deque
import heapq
import os
from Astar import Astar
from Bfs import BFS

from ParkingPuzzle import ParkingPuzzle

class main:
   
    def game_loop(puzzle, meta):
        """Permite al usuario interactuar con el rompecabezas moviendo vehículos."""
        while not puzzle.is_goal(meta):
            os.system("cls")
            print_board(puzzle.board)
            move = input("Introduce tu movimiento (ej. 'A L' para mover el vehículo A a la izquierda): ").strip().split()

            # Verificación de input:
            if len(move) != 2:
                print("Movimiento inválido. Intenta de nuevo.")
                continue
            
            vehicle_id, direction = move
            if vehicle_id not in puzzle.vehicles or direction not in ('L', 'R', 'U', 'D'):
                print("Movimiento inválido. Intenta de nuevo.")
                continue

            new_puzzle, response = puzzle.move_vehicle((vehicle_id, direction))
            if new_puzzle and response:
                puzzle = new_puzzle
            else:
                print("Movimiento inválido. Intenta de nuevo.")
            
        print_board(puzzle.board)
        print("¡Felicidades! Has resuelto el rompecabezas.")
    
def load_board_from_file(filename):
    """Carga el tablero de un archivo de texto."""
    with open(filename, 'r') as file:
        board = [line.strip().split() for line in file.readlines()]
    return board

def print_board(board):
        """Imprime la representación del tablero en la consola."""
        for row in board:
            print(" ".join(row))
        print()

# Ejemplo de uso
board = load_board_from_file('nivel.txt')
puzzle = ParkingPuzzle(board)
meta = puzzle.goal_position

# Pesos de las heuristicas:
peso1, peso2, peso3 = 1, 1, 1

result = Astar.astar(puzzle, peso1, peso2, peso3,meta)

# result = BFS.bfs(puzzle,meta)
if result:
    print("Solución encontrada:")
    print(result)
else:
    print("No se encontró solución.")
