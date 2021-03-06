import pyomo.environ as pe
import pandas as pd

from sudoku_solver.cli import CLI
from sudoku_solver.conductor import Conductor


def main() -> pd.DataFrame:
    cli = CLI()
    cli.parse_args()

    conductor = Conductor(cli.args.model_inputs)
    conductor.solve_sudoku()

    return conductor.solver.solution_df


if __name__ == "__main__":
    main()
