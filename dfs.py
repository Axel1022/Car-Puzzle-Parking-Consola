import time
import psutil  # Para medir uso de memoria en sistemas Windows
from collections import deque

def bfs_shortest_paths(board, starts, goal):
    # Dimensiones del tablero
    rows = len(board)
    cols = len(board[0])


    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    queue = deque([(start, []) for start in starts])
    visited = set(starts)
    expanded_nodes = 0
    max_search_depth = 0

    while queue:
        (x, y), path = queue.popleft()
        expanded_nodes += 1
        max_search_depth = max(max_search_depth, len(path))

        if board[x][y] == goal:
            for px, py in path:
                board[px][py] = '*'
            return True, path, expanded_nodes, len(path), max_search_depth

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols and board[nx][ny] != '#' and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(x, y)]))

    return False, [], expanded_nodes, 0, max_search_depth

def read_board_from_file(filename):
    board = []
    with open(filename, 'r') as f:
        for line in f:
            board.append(line.strip().split())
    return board

def print_board(board):
    for row in board:
        print(' '.join(row))

def benchmark(board_file):
    board = read_board_from_file(board_file)

    starts = []
    goal = '0'

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'A':
                starts.append((i, j))

    if not starts:
        print("Error: No se encontró ninguna posición inicial 'A' en el tablero.")
        return

    print("Tablero inicial:")
    print_board(board)
    print()

    start_time = time.time()
    found, path, expanded_nodes, solution_depth, max_search_depth = bfs_shortest_paths(board, starts, goal)
    end_time = time.time()

    if found:
        print("Camino encontrado:")
        final_board = [row[:] for row in board]
        for px, py in path:
            final_board[px][py] = '*'
        print_board(final_board)
    else:
        print("No se encontró un camino válido hacia '{}' desde las posiciones iniciales 'A'.".format(goal))

    execution_time = end_time - start_time
    print(f"\nMétricas:")
    print(f"Número de movimientos (costo de la ruta): {solution_depth}")
    print(f"Cantidad de nodos expandidos: {expanded_nodes}")
    print(f"Profundidad de la solución: {solution_depth}")
    print(f"Máxima profundidad de la búsqueda: {max_search_depth}")
    print(f"Tiempo de ejecución: {execution_time:.6f} segundos")

    max_memory_usage = psutil.Process().memory_info().rss / 1024.0 / 1024.0  # En MB
    print(f"Máxima memoria RAM consumida durante la ejecución: {max_memory_usage:.2f} MB")

# Ejemplo de uso
if __name__ == "__main__":
    board_file = "tablero.txt"
    benchmark(board_file)
