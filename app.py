"""
Streamlit UI
"""
import numpy as np
import pandas as pd
import streamlit as st

from sudoku.create_input_data import create_input_data
from sudoku.sudoku import create_and_solve


@st.cache_data
def create_input_data_list(input_data_df: pd.DataFrame) -> None:
    """
    
    """
    flattened = input_data_df.to_numpy().flatten()

    box_mapping = {
        (0, 0): 1, (0, 1): 2, (0, 2): 3,
        (1, 0): 4, (1, 1): 5, (1, 2): 6,
        (2, 0): 7, (2, 1): 8, (2, 2): 9
    }

    input_data_dicts = []
    for idx, i in enumerate(flattened):
        if not np.isnan(i):
            row = (idx // 9) + 1
            column = (idx % 9) + 1
            value = i

            box_row = (row - 1) // 3
            box_col = (column - 1) // 3

            box = box_mapping[(box_row, box_col)]

            input_data_dicts.append(
                {
                    "row": row, "column": column, "box": box, "value": value
                }
            )

    pyomo_input_data = create_input_data(input_data_dicts)

    st.session_state.pyomo_inputs = pyomo_input_data

    st.success("Input puzzle loaded!")

    st.session_state.input_puzzle_is_loaded = True


@st.cache_data
def solve_puzzle(input_data: list) -> None:
    """
    Solve the sudoku puzzle and return the results
    """
    solution = create_and_solve(input_data)
    st.session_state.solved_results = solution
    st.session_state.puzzle_is_solved = True


st.title("Sudoku solver")

if "unsolved_puzzle" not in st.session_state:
    st.session_state.unsolved_puzzle = None

if "input_puzzle_is_loaded" not in st.session_state:
    st.session_state.input_puzzle_is_loaded = False

if "pyomo_inputs" not in st.session_state:
    st.session_state.pyomo_inputs = None

if "puzzle_is_solved" not in st.session_state:
    st.session_state.puzzle_is_solved = False

if "solved_results" not in st.session_state:
    st.session_state.solved_results = None


if not st.session_state.pyomo_inputs:
    blank_puzzle_df = pd.DataFrame(index=list(range(1, 10)), columns=list(range(1, 10)))
    st.session_state.unsolved_puzzle = st.data_editor(
        blank_puzzle_df,
        column_config={
            i: st.column_config.NumberColumn(
                f"{i}",
                min_value=1,
                max_value=9,
                step=1,
                format="%d"
            )
            for i in range(1, 10)
        }
    )

    st.button(
        "Create input data",
        on_click=create_input_data_list,
        args=(st.session_state.unsolved_puzzle,)
    )

if st.session_state.pyomo_inputs and st.session_state.input_puzzle_is_loaded and not st.session_state.puzzle_is_solved:
    st.dataframe(st.session_state.unsolved_puzzle.fillna(''))
    st.button("Solve", on_click=solve_puzzle, args=(st.session_state.pyomo_inputs,))

if st.session_state.puzzle_is_solved:
    st.dataframe(pd.DataFrame(st.session_state.solved_results))
