"""
Conducts all necessary actions for the tool
"""
from sudoku_solver.solver import Solver
from sudoku_solver.sudoku_model import SudokuModel


class Conductor:
    """
    Conducts all necessary actions for the tool

    Args:
        model_inputs (dict): Dictionary of inputs for the pyomo model

    Attributes:
        sudoku_model (SudokuModel): Instance of the SudokuModel class
        solver (Solver): Instance of the Solver class

    Methods:
        solve_sudoku (None): Solves an input sudoku puzzle
    """
    def __init__(self, model_inputs: dict):
        self._model_inputs: dict = model_inputs

        self.sudoku_model: SudokuModel = SudokuModel()
        self.solver: Solver = None

    def solve_sudoku(self) -> None:
        """
        Solves the sudoku puzzle

        Args:
            None

        Returns:
            None
        """
        self.sudoku_model.create_model()

        self.solver = Solver(self.sudoku_model.model, self._model_inputs, False)
        self.solver.calculate_solution()
