"""
Includes unit tests for InputsFormatter
"""
import unittest
from unittest.mock import Mock, patch

from sudoku_solver.inputs_formatter import InputsFormatter


class TestInputsFormatter(unittest.TestCase):
    def setUp(self):
        self.inputs = {(1, 2): 100, (2, 2): 200}
        self.inputs_formatter = InputsFormatter(self.inputs)

    @patch("sudoku_solver.inputs_formatter.InputsFormatter._format_defaults")
    @patch("sudoku_solver.inputs_formatter.InputsFormatter._format_inputs")
    def test_set_formatted_inputs(
            self,
            mock_format_inputs: Mock,
            mock_format_defaults: Mock
    ):
        self.inputs_formatter.set_formatted_inputs()
        mock_format_inputs.assert_called_once()
        mock_format_defaults.assert_called_once()

    def test_format_inputs(self):
        self.inputs_formatter._format_inputs()

        self.assertDictEqual(
            self.inputs_formatter.formatted_inputs,
            {None: {"given_vals": {(1, 2, 100): 1, (2, 2, 200): 1}}}
        )

    def test_format_defaults(self):
        self.inputs_formatter.formatted_inputs = {None: {1: 100}}

        self.inputs_formatter._format_defaults()

        self.assertDictEqual(
            self.inputs_formatter.formatted_inputs,
            {None: {
                1: 100,
                "rows": {None: list(range(1, 10))},
                "cols": {None: list(range(1, 10))},
                "vals": {None: list(range(1, 10))},
                "p": {None: list(range(1, 4))},
                "q": {None: list(range(1, 4))},
                "square_size": {None: 3},
            }}
        )
