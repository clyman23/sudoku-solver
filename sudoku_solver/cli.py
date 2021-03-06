"""
CLI module
"""
import argparse


class CLI:
    """
    CLI module

    Args:
        None

    Attributes:
        parser (argparse.ArgumentParser): Argument parser

    Methods:
        parse_args (None): Parse input arguments
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.args = None

    def parse_args(self) -> None:
        """
        Parse input arguments to CLI

        Args:
            None

        Returns:
            None
        """
        self.parser.add_argument(
            "model_inputs",
            help="Tuple-int dictionary of given sudoku board inputs",
            type=dict
        )

        self.args = self.parser.parse_args()
