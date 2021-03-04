"""
Creates pyomo AbstractModel of Sudoku board to be solved
"""
import pyomo.environ as pe


class SudokuModel:
    """
    Creates pyomo AbstractModel of Sudoku board to be solved

    Args:
        None

    Attributes:
        model (pe.AbstractModel): The pyomo model to solve

    Methods:
        create_model (None): Creates the pyomo AbstractModel to solve
    """
    def __init__(self):
        self.model: pe.AbstractModel = pe.AbstractModel()

    def create_model(self) -> None:
        """
        Creates the pyomo AbstractModel to solve

        Args:
            None

        Returns:
            None
        """
        self._create_sets()
        self._create_params()
        self._create_vars()
        self._create_constraints()
        self._create_obj()

    def _create_sets(self) -> None:
        self.model.rows = pe.Set()
        self.model.cols = pe.Set()
        self.model.vals = pe.Set()

        self.model.p = pe.Set()
        self.model.q = pe.Set()

    def _create_params(self) -> None:
        self.model.square_size = pe.Param() # 3
        self.model.given_vals = pe.Param(
            self.model.rows,
            self.model.cols,
            self.model.vals,
            default=0,
            domain=pe.Binary
        )

    def _create_vars(self) -> None:
        self.model.solved_grid = pe.Var(
            self.model.rows,
            self.model.cols,
            self.model.vals,
            domain=pe.Binary
        )

    def _create_constraints(self) -> None:
        self.model.row_cons = pe.Constraint(
            self.model.cols,
            self.model.vals,
            rule=self._row_cons_rule
        )

        self.model.col_cons = pe.Constraint(
            self.model.rows,
            self.model.vals,
            rule=self._col_cons_rule
        )

        self.model.square_cons = pe.Constraint(
            self.model.p,
            self.model.q,
            rule=self._square_cons_rule
        )

        self.model.no_zeros_cons = pe.Constraint(
            self.model.rows,
            self.model.cols,
            rule=self._no_zeros_cons_rule
        )

        self.model.given_vals_cons = pe.Constraint(
            self.model.rows,
            self.model.cols,
            self.model.vals,
            rule=self._given_vals_cons_rule
        )

    @staticmethod
    def _row_cons_rule(_model, _col, _val) -> bool:
        return sum([_model.solved_grid[r, _col, _val] for r in _model.rows.data()]) == 1

    @staticmethod
    def _col_cons_rule(_model, _row, _val) -> bool:
        return sum([_model.solved_grid[_row, c, _val] for c in _model.cols.data()]) == 1

    @staticmethod
    def _square_cons_rule(_model, _p, _q) -> bool:
        return sum([
            _model.solved_grid[3*_p - (3*_p - 2), 3*_q - (3*_q - 2), v] for v in _model.vals.data()
        ]) == 1

    @staticmethod
    def _no_zeros_cons_rule(_model, _row, _col) -> bool:
        return sum([_model.solved_grid[_row, _col, v] for v in _model.vals.data()]) == 1

    @staticmethod
    def _given_vals_cons_rule(_model, _row, _col, _val) -> bool:
        if _model.given_vals[_row, _col, _val] == 1:
            return _model.solved_grid[_row, _col, _val] == _model.given_vals[_row, _col, _val]
        return pe.Constraint.Skip

    def _create_obj(self) -> None:
        self.model.obj = pe.Objective(expr=1)

