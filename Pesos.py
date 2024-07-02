import itertools
import numpy as np
from Astar import Astar

class Pesos:

    @staticmethod
    def evaluate_weights(weights, puzzle, meta):
        """Evalúa un conjunto de pesos ejecutando A* y midiendo el costo del camino encontrado."""
        try:
            result = Astar.astar(puzzle, meta, *weights)
            if result is not None:
                return result['cost_of_path']
        except Exception as e:
            print(f"Error al evaluar pesos {weights}: {e}")
        return float('inf')

    @staticmethod
    def grid_search(puzzle, meta, num_heuristics=5):
        """Realiza una búsqueda en cuadrícula para encontrar los mejores pesos."""
        weight_ranges = [np.arange(0, 1.1, 0.1) for _ in range(num_heuristics)]
        best_score = float('inf')
        best_weights = None

        for weights in itertools.product(*weight_ranges):
            score = Pesos.evaluate_weights(weights, puzzle, meta)
            if score < best_score:
                best_score = score
                best_weights = weights

        return best_weights, best_score
