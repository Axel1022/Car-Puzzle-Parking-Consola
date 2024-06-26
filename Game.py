import sys
from collections import deque
import heapq
import time
import psutil
import os

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
        print (posiciones)
        return posiciones

class ParkingPuzzle:
    def __init__(self, board):
        self.board = board
        self.vehicles = self.extract_vehicles()
        self.goal_position = self.find_goal_position()
        self.path = []
        self.profundidad = 0


    def extract_vehicles(self):
        """Extrae los vehículos del tablero y los almacena en un diccionario."""
        vehiculos = {}
        for fila in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[fila][col] != '.' and self.board[fila][col] != '0':
                    id = self.board[fila][col]
                    if id not in vehiculos:
                        if col < len(self.board[0]) - 1 and self.board[fila][col + 1] == id:
                            orientacion = 'H'
                            longitud = 1
                            while col + longitud < len(self.board[0]) and self.board[fila][col + longitud] == id:
                                longitud += 1
                        else:
                            orientacion = 'V'
                            longitud = 1
                            while fila + longitud < len(self.board) and self.board[fila + longitud][col] == id:
                                longitud += 1
                        vehiculos[id] = Vehiculo(id, orientacion, longitud, fila, col)
        return vehiculos

    def find_goal_position(self):
        """Encuentra la posición del objetivo (representada por '0') en el tablero."""
        for fila in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[fila][col] == '0':
                    return (fila, col)
        return None

    def is_goal(self,meta):
        """Verifica si el vehículo del jugador ha alcanzado la posición objetivo."""
        player_vehicle = self.vehicles['A']
        player_positions = player_vehicle.get_positions()

        for pos in player_positions:

        # Comprobar si alguna posición del vehículo A coincide con la meta
            if pos == meta:
                return True
        return False

    def get_possible_moves(self):
        """Obtiene todos los movimientos posibles para todos los vehículos."""
        moves = []
        for vehicle in self.vehicles.values():
            if vehicle.orientacion == 'H':
                if vehicle.col > 0 and self.board[vehicle.fila][vehicle.col - 1] == '.':
                    moves.append((vehicle.id, 'L'))
                if vehicle.col + vehicle.longitud < len(self.board[0]) and self.board[vehicle.fila][vehicle.col + vehicle.longitud] == '.':
                    moves.append((vehicle.id, 'R'))
            else:
                if vehicle.fila > 0 and self.board[vehicle.fila - 1][vehicle.col] == '.':
                    moves.append((vehicle.id, 'U'))
                if vehicle.fila + vehicle.longitud < len(self.board) and self.board[vehicle.fila + vehicle.longitud][vehicle.col] == '.':
                    moves.append((vehicle.id, 'D'))
        return moves

    def move_vehicle(self, move):
        """Mueve un vehículo en el tablero y devuelve un nuevo estado del puzzle."""
        new_board = [fila[:] for fila in self.board]
        # print (self.vehicles.items())
        vehicle = self.vehicles[move[0]]
        direction = move[1]

        response = True

        positions = vehicle.get_positions()

        if direction == 'L':
            if vehicle.orientacion == 'H':
                if vehicle.col > 0 and (new_board[vehicle.fila][vehicle.col - 1] == '.') or new_board[vehicle.fila][vehicle.col - 1] == '0':
                    for pos in positions:
                        new_board[pos[0]][pos[1] - 1] = vehicle.id
                    new_board[positions[-1][0]][positions[-1][1]] = '.'
                    vehicle.col -= 1
                else:
                    response = False

        elif direction == 'R':
            if vehicle.orientacion == 'H':
                if vehicle.col + vehicle.longitud < len(new_board[0]) and (new_board[vehicle.fila][vehicle.col + vehicle.longitud] == '.') or new_board[vehicle.fila][vehicle.col + vehicle.longitud] == '0':
                    for pos in reversed(positions):
                        new_board[pos[0]][pos[1] + 1] = vehicle.id
                    new_board[positions[0][0]][positions[0][1]] = '.'
                    vehicle.col += 1
                else:
                    response = False

        elif direction == 'U':
            if vehicle.orientacion == 'V':
                if vehicle.fila > 0 and (new_board[vehicle.fila - 1][vehicle.col] == '.') or new_board[vehicle.fila - 1][vehicle.col] == '0':
                    for pos in positions:
                        new_board[pos[0] - 1][pos[1]] = vehicle.id
                    new_board[positions[-1][0]][positions[-1][1]] = '.'
                    vehicle.fila -= 1
                else:
                    response = False

        elif direction == 'D':
            if vehicle.orientacion == 'V':
                if vehicle.fila + vehicle.longitud < len(new_board) and (new_board[vehicle.fila + vehicle.longitud][vehicle.col] == '.') or new_board[vehicle.fila + vehicle.longitud][vehicle.col] == '0':
                    for pos in reversed(positions):
                        new_board[pos[0] + 1][pos[1]] = vehicle.id
                    new_board[positions[0][0]][positions[0][1]] = '.'
                    vehicle.fila += 1
                else:
                    response = False
        else:
            # Movimiento no permitido
            return None

        new_puzzle = ParkingPuzzle(new_board)
        new_puzzle.path = self.path + [move]
        new_puzzle.profundidad = self.profundidad + 1
        return new_puzzle,response

    def get_path(self):
        """Devuelve el camino recorrido hasta el estado actual."""
        return self.path

def bfs(puzzle):
    """Algoritmo de búsqueda en anchura."""
    start_time = time.time()
    frontier = deque([puzzle])
    explored = set()
    nodes_expanded = 0
    max_search_depth = 0

    while frontier:
        current_puzzle = frontier.popleft()
        nodes_expanded += 1

        if current_puzzle.is_goal():
            return generate_output(current_puzzle, nodes_expanded, max_search_depth, start_time)

        explored.add(tuple(map(tuple, current_puzzle.board)))

        for move in current_puzzle.get_possible_moves():
            new_puzzle = current_puzzle.move_vehicle(move)
            if tuple(map(tuple, new_puzzle.board)) not in explored:
                frontier.append(new_puzzle)
                max_search_depth = max(max_search_depth, new_puzzle.profundidad)

    return None

def astar(puzzle, w1, w2, w3):
    """Algoritmo A* con heurísticas combinadas."""
    start_time = time.time()
    frontier = []
    heapq.heappush(frontier, (0, puzzle))
    explored = set()
    nodes_expanded = 0
    max_search_depth = 0

    while frontier:
        _, current_puzzle = heapq.heappop(frontier)
        nodes_expanded += 1

        if current_puzzle.is_goal():
            return generate_output(current_puzzle, nodes_expanded, max_search_depth, start_time)

        explored.add(tuple(map(tuple, current_puzzle.board)))

        for move in current_puzzle.get_possible_moves():
            new_puzzle = current_puzzle.move_vehicle(move)
            if tuple(map(tuple, new_puzzle.board)) not in explored:
                cost = new_puzzle.profundidad + w1 * heuristic1(new_puzzle) + w2 * heuristic2(new_puzzle) + w3 * heuristic3(new_puzzle)
                heapq.heappush(frontier, (cost, new_puzzle))
                max_search_depth = max(max_search_depth, new_puzzle.profundidad)

    return None

def heuristic1(puzzle):
    """Ejemplo de heurística simple."""
    player_vehicle = puzzle.vehicles['A']
    return abs(player_vehicle.fila - puzzle.goal_position[0]) + abs(player_vehicle.col - puzzle.goal_position[1])

def heuristic2(puzzle):
    """Segunda heurística: número de vehículos bloqueando la salida."""
    blocking_vehicles = 0
    player_vehicle = puzzle.vehicles['A']
    if player_vehicle.orientacion == 'H':
        for col in range(player_vehicle.col + player_vehicle.longitud, len(puzzle.board[0])):
            if puzzle.board[player_vehicle.fila][col] != '.':
                blocking_vehicles += 1
    return blocking_vehicles

def heuristic3(puzzle):
    """Tercera heurística: suma de distancias de todos los vehículos a sus posiciones objetivo."""
    distance_sum = 0
    for vehicle in puzzle.vehicles.values():
        if vehicle.orientacion == 'H':
            distance_sum += abs(vehicle.col - puzzle.goal_position[1])
        else:
            distance_sum += abs(vehicle.fila - puzzle.goal_position[0])
    return distance_sum

def generate_output(puzzle, nodes_expanded, max_search_depth, start_time):
    """Genera el output final del algoritmo."""
    elapsed_time = time.time() - start_time
    memory_usage = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
    return {
        'path_to_goal': puzzle.get_path(),
        'cost_of_path': len(puzzle.get_path()),
        'nodes_expanded': nodes_expanded,
        'search_depth': len(puzzle.get_path()),
        'max_search_depth': max_search_depth,
        'running_time': elapsed_time,
        'max_ram_usage': memory_usage
    }

def print_board(board):
    """Imprime la representación del tablero en la consola."""
    for row in board:
        print(" ".join(row))
    print()

def game_loop(puzzle,meta):
    """Permite al usuario interactuar con el rompecabezas moviendo vehículos."""
    while not puzzle.is_goal(meta):
        os.system("cls")
        print_board(puzzle.board)
        move = input("Introduce tu movimiento (ej. 'A L' para mover el vehículo A a la izquierda): ").strip().split()

        # Verificacion de input:
        if len(move) != 2:
            print("Movimiento inválido. Intenta de nuevo.")
            continue
        
        vehicle_id, direction = move
        if vehicle_id not in puzzle.vehicles or direction not in ('L', 'R', 'U', 'D'):
            print("Movimiento inválido. Intenta de nuevo.")
            continue

        new_puzzle,response = puzzle.move_vehicle((vehicle_id, direction))
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

# Ejemplo de uso
board = load_board_from_file('nivel.txt')
puzzle = ParkingPuzzle(board)
meta = puzzle.goal_position

game_loop(puzzle,meta)
