import pyomo.environ as pe
import pandas as pd

from sudoku_solver.conductor import Conductor


def main(inputs: dict) -> pd.DataFrame:
    conductor = Conductor(inputs)
    conductor.solve_sudoku()

    return conductor.solver.solution_df


if __name__ == "__main__":
    inputs = {
        None: {
            "rows": {None: list(range(1, 10))},
            "cols": {None: list(range(1, 10))},
            "vals": {None: list(range(1, 10))},
            "p": {None: list(range(1, 4))},
            "q": {None: list(range(1, 4))},
            "square_size": {None: 3},
            "given_vals": {
                (1, 7, 2): 1,
                (2, 2, 8): 1,
                (2, 6, 7): 1,
                (2, 8, 9): 1,
                (3, 1, 6): 1,
                (3, 3, 2): 1,
                (3, 7, 5): 1,
                (4, 2, 7): 1,
                (4, 5, 6): 1,
                (5, 4, 9): 1,
                (5, 6, 1): 1,
                (6, 5, 2): 1, 
                (6, 8, 4): 1,
                (7, 3, 5): 1,
                (7, 7, 6): 1,
                (7, 9, 3): 1,
                (8, 2, 9): 1,
                (8, 4, 4): 1,
                (8, 8, 7): 1,
                (9, 3, 6): 1,
            },
        },
    }

    main(inputs)
