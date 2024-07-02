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
