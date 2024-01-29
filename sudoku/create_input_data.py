"""
Create input formatted for pyomo from a dictionary of known sudoku squares
"""
import itertools

def create_input_data(knowns: list) -> dict:
    """
    Given a dict of knowns, create a formatted pyomo dict
    """
    location_index = []

    box_mapping = {
        (0, 0): 1, (0, 1): 2, (0, 2): 3,
        (1, 0): 4, (1, 1): 5, (1, 2): 6,
        (2, 0): 7, (2, 1): 8, (2, 2): 9
    }

    row_col_combos = [i for i in itertools.product(list(range(1, 10)), list(range(1, 10)))]
    for location in row_col_combos:
        box_row = (location[0] - 1) // 3
        box_col = (location[1] - 1) // 3
        location_index.append(location + (box_mapping[(box_row, box_col)],) )

    data = {
        None: {
            "h": {None: list(range(1, 10))},
            "i": {None: list(range(1, 10))},
            "j": {None: list(range(1, 10))},
            "k": {None: list(range(1, 10))},
            "location_index": {None: location_index},
        }
    }

    data[None]["knowns"] = {
        (known["value"], (known["row"], known["column"], known["box"])): 1
        for known in knowns
    }

    return data
