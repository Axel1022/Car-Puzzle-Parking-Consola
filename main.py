from collections import deque
import heapq
import os
from Astar import Astar
from Bfs import BFS
from ParkingPuzzle import ParkingPuzzle

class Main:

    @staticmethod
    def game_loop(puzzle, meta):
        """Permite al usuario interactuar con el rompecabezas moviendo vehículos."""
        while not puzzle.is_goal(meta):
            os.system("cls" if os.name == "nt" else "clear")
            Main.print_board(puzzle.board)
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

        Main.print_board(puzzle.board)
        print("¡Felicidades! Has resuelto el rompecabezas.")

    @staticmethod
    def load_board_from_file(filename):
        """Carga el tablero de un archivo de texto."""
        with open(filename, 'r') as file:
            board = [line.strip().split() for line in file.readlines()]
        return board

    @staticmethod
    def print_board(board):
        """Imprime la representación del tablero en la consola."""
        for row in board:
            print(" ".join(row))
        print()

    @staticmethod
    def main_menu():
        """Muestra el menú principal e interactúa con el usuario."""
        while True:
            print("Seleccione una opción:")
            print("1. Resolver con A*")
            print("2. Resolver con BFS")
            print("3. Jugar manualmente")
            print("4. Salir")
            choice = input("Opción: ").strip()

            if choice not in ['1', '2', '3', '4']:
                print("Opción inválida. Intenta de nuevo.")
                continue

            if choice == '4':
                print("Saliendo...")
                break

            filename = input("Introduce el nombre del archivo del tablero (ej. 'nivel1'): ").strip() + '.txt'
            board = Main.load_board_from_file(filename)
            puzzle = ParkingPuzzle(board)
            meta = puzzle.goal_position

            if choice == '1':
                print("Resolviendo con A*...")
                peso1, peso2, peso3 = 1, 1, 1
                result = Astar.astar(puzzle, peso1, peso2, peso3, meta)
                Main.handle_result(result, "AstarResultbenchmark.txt")
            elif choice == '2':
                print("Resolviendo con BFS...")
                result = BFS.bfs(puzzle)
                Main.handle_result(result, "BFSResultbenchmark.txt")
            elif choice == '3':
                Main.game_loop(puzzle, meta)

    @staticmethod
    def handle_result(result, filename):
        """Maneja los resultados de la solución del rompecabezas."""
        if result:
            with open(filename, 'w+') as file:
                file.writelines("Ultima corrida:\n")
                for key, value in result.items():
                    if key not in ["max_ram_usage", "running_time"]:
                        file.write(f"{key}: {value}\n")
                    else:
                        file.write(f"{key}: {value:.4f} \n")
            print(f"Resultados guardados en {filename}")
        else:
            print("No se encontró solución.")

if __name__ == "__main__":
    Main.main_menu()
