import numpy as np
import pyomo.environ as pe


def main():
    model = create_model()
    instance = instantiate_model(model)
    solve_model(instance)
    

def create_model():
    model = pe.AbstractModel()

    model.h = pe.Set() # The cell's number
    model.i = pe.Set() # The row
    model.j = pe.Set() # The column

    model.knowns = pe.Param(model.h, model.i, model.j, default=0)

    model.x = pe.Var(model.h, model.i, model.j, domain=pe.NonNegativeReals)

    model.knowns_constraint = pe.Constraint(model.h, model.i, model.j, rule=knowns_constraint)
    model.supply = pe.Constraint(model.h, rule=supply_constraint)
    model.col_constraint = pe.Constraint(model.h, model.j, rule=col_constraint)
    model.row_constraint = pe.Constraint(model.h, model.i, rule=row_constraint)
    model.demand = pe.Constraint(model.i, model.j, rule=demand_constraint)

    #TODO: Add constraint for 3x3... there are constraints on each "box"

    model.obj = pe.Objective(rule=objective_rule, sense=pe.minimize)

    return model

def knowns_constraint(m, h, i, j):
    if m.knowns[h, i, j]:
       return m.x[h, i, j] == 1
    else:
        return pe.Constraint.Skip

def supply_constraint(m, h):
    expr = 0
    for i in m.i:
        for j in m.j:
            expr += m.x[h, i, j]

    return expr == 3

def col_constraint(m, h, j):
    return sum(m.x[h, i, j] for i in m.i) == 1

def row_constraint(m, h, i):
    return sum(m.x[h, i, j] for j in m.j) == 1

def demand_constraint(m, i, j):
    return sum(-m.x[h, i, j] for h in m.j) == -1

def objective_rule(m):
    return pe.summation(m.x)


def instantiate_model(model):
    data = {
        None: {
            "h": {None: [1, 2, 3]},
            "i": {None: [1, 2, 3]},
            "j": {None: [1, 2, 3]},
            "knowns": {
                (2, 1, 1): 1,
                (1, 3, 3): 1
            }
        }
    }

    instance = model.create_instance(data)
    # instance.pprint()
    return instance


def solve_model(instance):
    solver = pe.SolverFactory("cbc")
    solver.solve(instance)

    instance.pprint()

    for index in instance.x:
        if instance.x[index].value == 1:
            print(index)

    solution_space = np.zeros((3, 3))

    for index in instance.x:
        if instance.x[index].value == 1:
            solution_space[index[1]-1, index[2]-1] = index[0]

    print()
    print(solution_space)


if __name__ == "__main__":
    main()
