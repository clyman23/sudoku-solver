"""
Contains end-to-end test for sudoku-solver
"""
import unittest
from unittest.mock import Mock, patch

import pandas as pd

from sudoku_solver.run import main


class TestE2E(unittest.TestCase):
    def setUp(self):
        self.inputs = {
            (1, 7): 2,
            (2, 2): 8,
            (2, 6): 7,
            (2, 8): 9,
            (3, 1): 6,
            (3, 3): 2,
            (3, 7): 5,
            (4, 2): 7,
            (4, 5): 6,
            (5, 4): 9,
            (5, 6): 1,
            (6, 5): 2, 
            (6, 8): 4,
            (7, 3): 5,
            (7, 7): 6,
            (7, 9): 3,
            (8, 2): 9,
            (8, 4): 4,
            (8, 8): 7,
            (9, 3): 6,
        }

    @patch("sudoku_solver.run.CLI")
    def test_e2e(self, mock_cli: Mock):
        mock_cli_instance = Mock()
        mock_cli.return_value = mock_cli_instance
        mock_cli_instance.args.model_inputs = self.inputs

        solution_df = main()

        expected_df = pd.DataFrame(
            {
                1: [5, 2, 6, 8, 7, 3, 9, 1, 4],
                2: [3, 8, 4, 7, 6, 5, 1, 9, 2],
                3: [9, 4, 2, 1, 8, 7, 5, 3, 6],
                4: [8, 5, 1, 2, 9, 6, 7, 4, 3],
                5: [7, 1, 9, 6, 3, 2, 4, 5, 8],
                6: [4, 7, 8, 3, 1, 9, 2, 6, 5],
                7: [2, 3, 5, 9, 4, 1, 6, 8, 7],
                8: [6, 9, 3, 5, 2, 4, 8, 7, 1],
                9: [1, 6, 7, 4, 5, 8, 3, 2, 9],
            },
            index=list(range(1, 10))
        )

        expected_df.index.name = "i"
        expected_df.columns.name = "j"

        pd.testing.assert_frame_equal(expected_df, solution_df)
