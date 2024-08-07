import sys
from collections import deque
import heapq
import time
import psutil
import os
from ParkingPuzzle import ParkingPuzzle

class Astar:

    @staticmethod
    def astar(puzzle, meta, *weights):
        """Algoritmo A* con heurísticas combinadas."""
        start_time = time.time()
        heuristics = [heuristic1, heuristic2, heuristic3, heuristic4, heuristic5]
        weights = weights[:len(heuristics)]

        initial_cost = sum(w * h(puzzle, meta, [], []) for w, h in zip(weights, heuristics))
        frontier = []
        counter = 0  # Contador para desempate
        heapq.heappush(frontier, (initial_cost, counter, puzzle, []))  # Añadimos lista de movimientos anteriores
        explored = set()
        nodes_expanded = 0
        max_search_depth = 0

        while frontier:
            _, _, current_puzzle, previous_moves = heapq.heappop(frontier)
            nodes_expanded += 1

            if current_puzzle.is_goal(meta):
                return generate_output(current_puzzle, nodes_expanded, max_search_depth, start_time)

            explored.add(tuple(map(tuple, current_puzzle.board)))

            for move in current_puzzle.get_possible_moves(meta):
                new_puzzle, response = current_puzzle.move_vehicle(move)
                if response and tuple(map(tuple, new_puzzle.board)) not in explored:
                    cost = (new_puzzle.profundidad +
                            sum(w * h(new_puzzle, meta, previous_moves, move) for w, h in zip(weights, heuristics)))
                    counter += 1
                    heapq.heappush(frontier, (cost, counter, new_puzzle, previous_moves + [move]))
                    max_search_depth = max(max_search_depth, new_puzzle.profundidad)

        return None

def heuristic1(puzzle, meta, *args):
    """Heurística que estima la menor cantidad de movimientos hasta la meta."""
    player_vehicle = puzzle.vehicles['A']

    # Calcula la distancia horizontal o vertical desde el vehículo 'A' hasta la meta
    if player_vehicle.orientacion == 'H':
        dist_to_goal = abs(player_vehicle.col + player_vehicle.longitud - meta[1])
    else:
        dist_to_goal = abs(player_vehicle.fila + player_vehicle.longitud - meta[0])

    return dist_to_goal

def heuristic2(puzzle, *args):
    """Segunda heurística: número de vehículos bloqueando la salida."""
    blocking_vehicles = 0
    player_vehicle = puzzle.vehicles['A']
    if player_vehicle.orientacion == 'H':
        for col in range(player_vehicle.col + player_vehicle.longitud, len(puzzle.board[0])):
            if puzzle.board[player_vehicle.fila][col] != '.':
                blocking_vehicles += 1
    else:
        for fila in range(player_vehicle.fila + player_vehicle.longitud, len(puzzle.board)):
            if puzzle.board[fila][player_vehicle.col] != '.':
                blocking_vehicles += 1
    return blocking_vehicles

def heuristic3(puzzle, meta, *args):
    """Tercera heurística: suma de distancias de todos los vehículos a sus posiciones objetivo."""
    distance_sum = 0
    for vehicle in puzzle.vehicles.values():
        if vehicle.orientacion == 'H':
            distance_sum += abs(vehicle.col - meta[1])
        else:
            distance_sum += abs(vehicle.fila - meta[0])
    return distance_sum

def heuristic4(puzzle, meta, previous_moves, current_move):
    """Heurística para evitar movimientos redundantes."""
    player_vehicle = puzzle.vehicles['A']
    player_positions = player_vehicle.get_positions()
    goal_row, goal_col = meta
    player_head_pos = player_positions[0]  # Posición inicial del vehículo del jugador

    # Distancia Manhattan desde la cabeza del vehículo del jugador hasta la meta
    dist_manhattan = abs(player_head_pos[0] - goal_row) + abs(player_head_pos[1] - goal_col)

    # Penalización por movimientos redundantes
    penalization_redundancy = 0
    if len(previous_moves) > 0:
        last_move = previous_moves[-1]
        if (current_move[0] == last_move[0] and
                ((current_move[1] == 'L' and last_move[1] == 'R') or
                 (current_move[1] == 'R' and last_move[1] == 'L') or
                 (current_move[1] == 'U' and last_move[1] == 'D') or
                 (current_move[1] == 'D' and last_move[1] == 'U'))):
            penalization_redundancy = 10  # Penalización alta para evitar movimientos redundantes

    return dist_manhattan + penalization_redundancy

def heuristic5(puzzle, meta, *args):
    """Penaliza cualquier estado donde un vehículo diferente a 'A' esté en la posición de la meta."""
    for vehicle_id, vehicle in puzzle.vehicles.items():
        if vehicle_id != 'A':
            if meta in vehicle.get_positions():
                return 1000  # Penalización alta para evitar que otros vehículos bloqueen la meta
    return 0

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
