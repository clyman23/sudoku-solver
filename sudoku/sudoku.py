import itertools
import json

import numpy as np
import pyomo.environ as pe

from sudoku.create_input_data import create_input_data


def main():
    with open("./examples/example_puzzle.json", "r") as f:
        knowns = json.load(f)
    data = create_input_data(knowns)

    create_and_solve(data)


def create_and_solve(input_data: dict) -> np.array:
    """
    input_data (dict): Dict of input data formatted for pyomo
    """
    model = create_model()
    instance = instantiate_model(model, input_data)
    solution = solve_model(instance)
    return solution


def create_model():
    model = pe.AbstractModel()

    model.h = pe.Set() # The cell's value
    model.location_index = pe.Set() # The cell's location (row, col, box)
    model.i = pe.Set() # The row
    model.j = pe.Set() # The column
    model.k = pe.Set() # The "box"

    # The input data of known cell values
    model.knowns = pe.Param(model.h, model.location_index, default=0)

    # Our binary variable for cell values
    # (can set as NonNegativeReals because we have integer/binary supply and demand)
    model.x = pe.Var(model.h, model.location_index, domain=pe.NonNegativeReals)

    model.knowns_constraint = pe.Constraint(model.h, model.location_index, rule=knowns_constraint)
    model.supply = pe.Constraint(model.h, rule=supply_constraint)
    model.col_constraint = pe.Constraint(model.h, model.j, rule=col_constraint)
    model.row_constraint = pe.Constraint(model.h, model.i, rule=row_constraint)
    model.box_constraint = pe.Constraint(model.h, model.k, rule=box_constraint)
    model.demand = pe.Constraint(model.location_index, rule=demand_constraint)

    model.obj = pe.Objective(rule=objective_rule, sense=pe.minimize)

    return model

def knowns_constraint(m, h, i, j, k):
    """
    If we have input data for a given cell, set the variable to the value of the input data
    """
    if m.knowns[h, (i, j, k)]:
       return m.x[h, (i, j, k)] == 1
    else:
        return pe.Constraint.Skip

def supply_constraint(m, h):
    """
    The available supply is that each number (h) can occur 9 times across the available combo of
    row x column x box
    """
    return sum(m.x[h, loc] for loc in m.location_index) == 9

def col_constraint(m, h, j):
    """
    There can only be one of each value in a given column
    """
    expr = 0

    for loc in m.location_index:
        loc_col = loc[1]
        if j == loc_col:
            expr += m.x[h, loc]

    return expr == 1

def row_constraint(m, h, i):
    """
    There can only be on of each value in a given row
    """
    expr = 0

    for loc in m.location_index:
        loc_row = loc[0]
        if i == loc_row:
            expr += m.x[h, loc]

    return expr == 1

def box_constraint(m, h, k):
    """
    There can only be one of each value in a given box
    """
    expr = 0

    for loc in m.location_index:
        loc_box = loc[2]
        if k == loc_box:
            expr += m.x[h, loc]

    return expr == 1

def demand_constraint(m, i, j, k):
    """
    At each valid row x column x box, the total number of values assigned is exactly 1
    If the row x column x box is not valid (the row and col are not in that box), we set to 0
    """
    return sum(-m.x[h, (i, j, k)] for h in m.h) == -1


def objective_rule(m):
    return pe.summation(m.x)


def instantiate_model(model, input_data):
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

    instance = model.create_instance(input_data)
    return instance


def solve_model(instance) -> np.array:
    solver = pe.SolverFactory("cbc")
    solver.solve(instance)

    instance.pprint()

    for index in instance.x:
        if instance.x[index].value == 1:
            print(index)

    solution_space = np.zeros((9, 9))

    for index in instance.x:
        if instance.x[index].value == 1:
            solution_space[index[1]-1, index[2]-1] = index[0]

    print()
    print(solution_space)
    return solution_space


if __name__ == "__main__":
    main()
