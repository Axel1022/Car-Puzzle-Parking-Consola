from Vehiculo import Vehiculo

class ParkingPuzzle:
    def __init__(self, board):
        self.board = board
        self.vehicles = self.extract_vehicles()
        print("Tablero cargado:")
        self.print_board()
        self.goal_position = self.find_goal_position()
     #   if self.goal_position is None:
       #     raise ValueError("No se encontró una posición objetivo en el tablero.")
        self.path = []
        self.profundidad = 0

    def print_board(self):
        for row in self.board:
            print(" ".join(row))
        print()

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

    def is_goal(self, meta):
        """Verifica si el vehículo del jugador ha alcanzado la posición objetivo."""
        player_vehicle = self.vehicles['A']
        player_positions = player_vehicle.get_positions()
        for pos in player_positions:
            if pos == meta:
                return True
        return False

    def get_possible_moves(self, meta):
        """Obtiene todos los movimientos posibles para todos los vehículos, priorizando los movimientos del vehículo del jugador."""
        moves = []
        player_vehicle_id = 'A'
        player_vehicle = self.vehicles[player_vehicle_id]

        # Obtener movimientos del vehículo del jugador primero
        if player_vehicle.orientacion == 'H':
            if player_vehicle.col < meta[1]:
                if player_vehicle.col + player_vehicle.longitud < len(self.board[0]) and (self.board[player_vehicle.fila][player_vehicle.col + player_vehicle.longitud] == '.' or self.board[player_vehicle.fila][player_vehicle.col + player_vehicle.longitud] == '0'):
                    moves.append((player_vehicle_id, 'R'))
            elif player_vehicle.col > meta[1]:
                if player_vehicle.col > 0 and (self.board[player_vehicle.fila][player_vehicle.col - 1] == '.' or self.board[player_vehicle.fila][player_vehicle.col - 1] == '0'):
                    moves.append((player_vehicle_id, 'L'))
        else:
            if player_vehicle.fila < meta[0]:
                if player_vehicle.fila + player_vehicle.longitud < len(self.board) and (self.board[player_vehicle.fila + player_vehicle.longitud][player_vehicle.col] == '.' or self.board[player_vehicle.fila + player_vehicle.longitud][player_vehicle.col] == '0'):
                    moves.append((player_vehicle_id, 'D'))
            elif player_vehicle.fila > meta[0]:
                if player_vehicle.fila > 0 and (self.board[player_vehicle.fila - 1][player_vehicle.col] == '.' or self.board[player_vehicle.fila - 1][player_vehicle.col] == '0'):
                    moves.append((player_vehicle_id, 'U'))

        # Solo continuar con los movimientos de otros vehículos si no hay movimientos posibles para el vehículo del jugador
        if not moves:
            for vehicle_id, vehicle in self.vehicles.items():
                if vehicle_id == player_vehicle_id:
                    continue
                if vehicle.orientacion == 'H':
                    if vehicle.col > 0 and (self.board[vehicle.fila][vehicle.col - 1] == '.' or self.board[vehicle.fila][vehicle.col - 1] == '0'):
                        moves.append((vehicle_id, 'L'))
                    if vehicle.col + vehicle.longitud < len(self.board[0]) and (self.board[vehicle.fila][vehicle.col + vehicle.longitud] == '.' or self.board[vehicle.fila][vehicle.col + vehicle.longitud] == '0'):
                        moves.append((vehicle_id, 'R'))
                else:
                    if vehicle.fila > 0 and (self.board[vehicle.fila - 1][vehicle.col] == '.' or self.board[vehicle.fila - 1][vehicle.col] == '0'):
                        moves.append((vehicle_id, 'U'))
                    if vehicle.fila + vehicle.longitud < len(self.board) and (self.board[vehicle.fila + vehicle.longitud][vehicle.col] == '.' or self.board[vehicle.fila + vehicle.longitud][vehicle.col] == '0'):
                        moves.append((vehicle_id, 'D'))
        return moves


    def move_vehicle(self, move):
        """Mueve un vehículo en el tablero y devuelve un nuevo estado del puzzle."""
        vehicle_id = move[0]
        if vehicle_id == 'B':
            return None, False  # No se puede mover el obstáculo 'B'

        new_board = [fila[:] for fila in self.board]
        vehicle = self.vehicles[vehicle_id]
        direction = move[1]

        response = True

        positions = vehicle.get_positions()

        if direction == 'L':
            if vehicle.orientacion == 'H':
                if vehicle.id == 'A' and vehicle.col > 0 and (new_board[vehicle.fila][vehicle.col - 1] == '.' or new_board[vehicle.fila][vehicle.col - 1] == '0'):
                    for pos in positions:
                        new_board[pos[0]][pos[1] - 1] = vehicle.id
                    new_board[positions[-1][0]][positions[-1][1]] = '.'
                    vehicle.col -= 1
                elif vehicle.id != 'A' and vehicle.col > 0 and new_board[vehicle.fila][vehicle.col - 1] == '.':
                    for pos in positions:
                        new_board[pos[0]][pos[1] - 1] = vehicle.id
                    new_board[positions[-1][0]][positions[-1][1]] = '.'
                    vehicle.col -= 1
                else:
                    response = False

        elif direction == 'R':
            if vehicle.orientacion == 'H':
                if vehicle.id == 'A' and vehicle.col + vehicle.longitud < len(new_board[0]) and (new_board[vehicle.fila][vehicle.col + vehicle.longitud] == '.' or new_board[vehicle.fila][vehicle.col + vehicle.longitud] == '0'):
                    for pos in reversed(positions):
                        new_board[pos[0]][pos[1] + 1] = vehicle.id
                    new_board[positions[0][0]][positions[0][1]] = '.'
                    vehicle.col += 1
                elif vehicle.id != 'A' and vehicle.col + vehicle.longitud < len(new_board[0]) and new_board[vehicle.fila][vehicle.col + vehicle.longitud] == '.':
                    for pos in reversed(positions):
                        new_board[pos[0]][pos[1] + 1] = vehicle.id
                    new_board[positions[0][0]][positions[0][1]] = '.'
                    vehicle.col += 1
                else:
                    response = False

        elif direction == 'U':
            if vehicle.orientacion == 'V':
                if vehicle.id == 'A' and vehicle.fila > 0 and (new_board[vehicle.fila - 1][vehicle.col] == '.' or new_board[vehicle.fila - 1][vehicle.col] == '0'):
                    for pos in positions:
                        new_board[pos[0] - 1][pos[1]] = vehicle.id
                    new_board[positions[-1][0]][positions[-1][1]] = '.'
                    vehicle.fila -= 1
                elif vehicle.id != 'A' and vehicle.fila > 0 and new_board[vehicle.fila - 1][vehicle.col] == '.':
                    for pos in positions:
                        new_board[pos[0] - 1][pos[1]] = vehicle.id
                    new_board[positions[-1][0]][positions[-1][1]] = '.'
                    vehicle.fila -= 1
                else:
                    response = False

        elif direction == 'D':
            if vehicle.orientacion == 'V':
                if vehicle.id == 'A' and vehicle.fila + vehicle.longitud < len(new_board) and (new_board[vehicle.fila + vehicle.longitud][vehicle.col] == '.' or new_board[vehicle.fila + vehicle.longitud][vehicle.col] == '0'):
                    for pos in reversed(positions):
                        new_board[pos[0] + 1][pos[1]] = vehicle.id
                    new_board[positions[0][0]][positions[0][1]] = '.'
                    vehicle.fila += 1
                elif vehicle.id != 'A' and vehicle.fila + vehicle.longitud < len(new_board) and new_board[vehicle.fila + vehicle.longitud][vehicle.col] == '.':
                    for pos in reversed(positions):
                        new_board[pos[0] + 1][pos[1]] = vehicle.id
                    new_board[positions[0][0]][positions[0][1]] = '.'
                    vehicle.fila += 1
                else:
                    response = False
        else:
            return None

        new_puzzle = ParkingPuzzle(new_board)
        new_puzzle.path = self.path + [move]
        new_puzzle.profundidad = self.profundidad + 1
        return new_puzzle, response

    def get_path(self):
        """Devuelve el camino recorrido hasta el estado actual."""
        return self.path
