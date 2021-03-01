"""
Contains class to solve a pyomo model based on given inputs
"""
import pyomo.environ as pe
import pandas as pd


class Solver:
    """
    Contains solver functions for pyomo model

    Args:
        model (pe.AbstractModel): The pyomo model to be solved
        model_inputs (dict): Dictionary of inputs formatted for creating pyomo model instance
        verbose_solve (bool): If True, pyomo solver prints out solver information

    Attributes:
        instance (pe.ConcreteModel): A concrete instance of the input model
        opt (pe.SolverFactory): The SolverFactory used for solving the model
        results (?): The output results status
        solution_df (pd.DataFrame): Output solutions formatted as a pandas DataFrame

    Methods:
        calculate_solution (None): Calculates the solution to the pyomo model instance
    """
    def __init__(self, model: pe.AbstractModel, model_inputs: dict, verbose_solve: bool):
        self._model: pe.AbstractModel = model
        self._model_inputs: dict = model_inputs
        self._verbose_solve: bool = verbose_solve

        self.instance: pe.ConcreteModel = None
        self.opt: pe.SolverFactory = pe.SolverFactory("glpk")
        self.results = None # What is datatype of opt.solve() return?

        self.solution_df: pd.DataFrame = pd.DataFrame()

    def calculate_solution(self) -> None:
        """
        Calculates the solution to the pyomo model instance

        Args:
            None

        Returns:
            None
        """
        self.instance = self._model.create_instance(self._model_inputs)
        self.results = self.opt.solve(self.instance, tee=self._verbose_solve)

        self._format_solution()

    def _format_solution(self) -> None:
        self.solution_df = pd.DataFrame({
            'i': [i[0] for i in self.instance.solved_grid.iterkeys()], 
            'j': [i[1] for i in self.instance.solved_grid.iterkeys()], 
            'k': [i[2] for i in self.instance.solved_grid.iterkeys()], 
            'assignment': [i.value for i in self.instance.solved_grid.itervalues()]
        })

        self.solution_df = self.solution_df[self.solution_df['assignment'] == 1]
        self.solution_df = self.solution_df.pivot(index = 'i', columns = 'j', values = 'k')
