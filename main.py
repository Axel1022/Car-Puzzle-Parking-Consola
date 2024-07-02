from collections import deque
import heapq
import os
from Astar import Astar
from Bfs import BFS
from Dfs import DFS
from ParkingPuzzle import ParkingPuzzle

import os.path

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
            while True:
                print("Seleccione una opción:")
                print("1. Resolver con A*")
                print("2. Resolver con BFS")
                print("3. Resolver con DFS")
                print("4. Jugar manualmente")
                print("5. Salir")
                choice = input("Opción: ").strip()
                if choice not in ['1', '2', '3', '4','5']:
                    os.system("cls")
                    print("Opción inválida. Intenta de nuevo.")
                else: break

            if choice == '5':
                print("Saliendo...")
                break
            os.system("cls")
            while True:
                filename = input("Introduce el nombre del archivo del tablero (ej. 'nivel1'): ").strip() + '.txt'
                if os.path.isfile(filename):
                    break
                else:
                    os.system("cls")
                    print(f"El archivo '{filename}' no existe. Inténtalo de nuevo.")

            board = Main.load_board_from_file(filename)
            puzzle = ParkingPuzzle(board)
            meta = puzzle.goal_position
            os.system('cls')
            if choice == '1':
                while True:
                    print("Seleccione la cantidad de heuristicas:")
                    print("1. 1")
                    print("2. 2")
                    print("3. 3")
                    print("4. 4")
                    print("5. 5")
                    choice = input("Opción: ").strip()
                    if choice not in ['1', '2', '3', '4', '5']:
                        os.system("cls")
                        print("Opción inválida. Intenta de nuevo.")
                    else:
                        peso1, peso2, peso3, peso4, peso5 = 3, 3.5, 2, 2, 2
                        # peso1, peso2, peso3, peso4, peso5 = 1, 1, 1, 1, 1
                        # peso1, peso2, peso3, peso4, peso5 = 2, 2, 4, 2, 1

                        print("Resolviendo con A*...")
                        if choice == "1":
                            result = Astar.astar(puzzle,meta, peso1)
                            Main.handle_result(result, "AstarResultbenchmark.txt")
                            break
                        elif choice == "2":
                            result = Astar.astar(puzzle, meta, peso1, peso2)
                            Main.handle_result(result, "AstarResultbenchmark.txt")
                            break
                        elif choice == "3":
                            result = Astar.astar(puzzle,meta, peso1,peso2,peso3)
                            Main.handle_result(result, "AstarResultbenchmark.txt")
                            break
                        elif choice == "4":
                            result = Astar.astar(puzzle,meta, peso1,peso2,peso3,peso4)
                            Main.handle_result(result, "AstarResultbenchmark.txt")
                            break
                        elif choice == "5":
                            result = Astar.astar(puzzle,meta, peso1,peso2,peso3,peso4,peso5)
                            Main.handle_result(result, "AstarResultbenchmark.txt")
                            break
                        else:
                            break

            elif choice == '2':
                print("Resolviendo con BFS...")
                result = BFS.bfs(puzzle,meta)
                Main.handle_result(result, "BFSResultbenchmark.txt")
            elif choice == '3':
                print("Resolviendo con DFS...")
                result = DFS.dfs(puzzle, meta)
                Main.handle_result(result, "DFSResultbenchmark.txt")


            elif choice == '4':
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