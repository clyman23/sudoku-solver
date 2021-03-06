"""
Formats model inputs for pyomo
"""
from typing import Dict, Tuple


class InputsFormatter:
    """
    Formats model inputs for pyomo

    Args:
        inputs (dict): Dictionary of tuple-int pairs of given sudoku board values

    Attribues:
        formatted_inputs (dict): Dictionary of model inputs formatted for pyomo

    Methods:
        set_formatted_inputs (None): Formats model inputs for pyomo
    """
    def __init__(self, inputs: Dict[Tuple[int, int], int]):
        self._inputs: dict = inputs

        self.formatted_inputs: dict = {}

    def set_formatted_inputs(self) -> None:
        """
        Formats model inputs for pyomo

        Args:
            None

        Returns:
            None
        """
        self._format_inputs()
        self._format_defaults()

    def _format_inputs(self) -> None:
        self.formatted_inputs[None] = {
            "given_vals": {i + (j,): 1 for i, j in self._inputs.items()},
        }

    def _format_defaults(self) -> None:
        self.formatted_inputs[None].update({
            "rows": {None: list(range(1, 10))},
            "cols": {None: list(range(1, 10))},
            "vals": {None: list(range(1, 10))},
            "p": {None: list(range(1, 4))},
            "q": {None: list(range(1, 4))},
            "square_size": {None: 3},
        })
