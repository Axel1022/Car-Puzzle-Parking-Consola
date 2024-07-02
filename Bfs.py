import time
import psutil
import os
from collections import deque
from ParkingPuzzle import ParkingPuzzle

class BFS:
    @staticmethod
    def bfs(puzzle, meta):
        """Algoritmo de Búsqueda en Anchura (BFS)"""
        start_time = time.time()
        frontier = deque([puzzle])
        explored = set()
        nodes_expanded = 0
        max_search_depth = 0

        while frontier:
            current_puzzle = frontier.popleft()
            nodes_expanded += 1

            if current_puzzle.is_goal(meta):
                return generate_output(current_puzzle, nodes_expanded, max_search_depth, start_time)

            explored.add(tuple(map(tuple, current_puzzle.board)))

            for move in current_puzzle.get_possible_moves(current_puzzle.goal_position):
                new_puzzle, response = current_puzzle.move_vehicle(move)
                if response and tuple(map(tuple, new_puzzle.board)) not in explored:
                    frontier.append(new_puzzle)
                    max_search_depth = max(max_search_depth, new_puzzle.profundidad)
                    explored.add(tuple(map(tuple, new_puzzle.board)))

        return None

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
