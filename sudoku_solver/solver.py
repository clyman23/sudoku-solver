import pyomo.environ as pe
import pandas as pd

model = pe.AbstractModel()

model.rows = pe.Set()
model.cols = pe.Set()
model.vals = pe.Set()

model.p = pe.Set()
model.q = pe.Set()

model.square_size = pe.Param() # 3

model.given_vals = pe.Param(model.rows, model.cols, model.vals, default=0, domain=pe.Binary)

model.solved_grid = pe.Var(model.rows, model.cols, model.vals, domain=pe.Binary)

def row_cons_rule(_model, _col, _val):
    return sum([_model.solved_grid[r, _col, _val] for r in _model.rows.data()]) == 1

model.row_cons = pe.Constraint(model.cols, model.vals, rule=row_cons_rule)

def col_cons_rule(_model, _row, _val):
    return sum([_model.solved_grid[_row, c, _val] for c in _model.cols.data()]) == 1

model.col_cons = pe.Constraint(model.rows, model.vals, rule=col_cons_rule)

def square_cons_rule(_model, _p, _q):
    return sum([
        _model.solved_grid[3*_p - (3*_p - 2), 3*_q - (3*_q - 2), v] for v in _model.vals.data()
    ]) == 1

model.square_cons = pe.Constraint(model.q, model.q)

def no_zeros_cons_rule(_model, _row, _col):
    return sum([_model.solved_grid[_row, _col, v] for v in _model.vals.data()]) == 1

model.no_zeros_cons = pe.Constraint(model.rows , model.cols, rule=no_zeros_cons_rule)

def given_vals_cons_rule(_model, _row, _col, _val):
    if _model.given_vals[_row, _col, _val] == 1:
        return _model.solved_grid[_row, _col, _val] == _model.given_vals[_row, _col, _val]
    return pe.Constraint.Skip

model.given_vals_cons = pe.Constraint(
    model.rows, model.cols, model.vals, rule=given_vals_cons_rule
)

model.obj = pe.Objective(expr=1)

# There seems to be an error thrown when pprint-ing an AbstractModel w/ a Param indexed by 3+ Sets
# model.pprint()


inputs = {
    None: {
        "rows": {None: list(range(1, 10))},
        "cols": {None: list(range(1, 10))},
        "vals": {None: list(range(1, 10))},
        "p": {None: list(range(1, 4))},
        "q": {None: list(range(1, 4))},
        "square_size": {None: 3},
        "given_vals": {
            (1, 7, 2): 1,
            (2, 2, 8): 1,
            (2, 6, 7): 1,
            (2, 8, 9): 1,
            (3, 1, 6): 1,
            (3, 3, 2): 1,
            (3, 7, 5): 1,
            (4, 2, 7): 1,
            (4, 5, 6): 1,
            (5, 4, 9): 1,
            (5, 6, 1): 1,
            (6, 5, 2): 1, 
            (6, 8, 4): 1,
            (7, 3, 5): 1,
            (7, 7, 6): 1,
            (7, 9, 3): 1,
            (8, 2, 9): 1,
            (8, 4, 4): 1,
            (8, 8, 7): 1,
            (9, 3, 6): 1,
        },
    },
}

instance = model.create_instance(inputs)


opt = pe.SolverFactory("glpk")
results = opt.solve(instance, tee=True)

print(results.solver.status)


solutionDf = pd.DataFrame({
    'i': [i[0] for i in instance.solved_grid.iterkeys()], 
    'j': [i[1] for i in instance.solved_grid.iterkeys()], 
    'k': [i[2] for i in instance.solved_grid.iterkeys()], 
    'assignment': [i.value for i in instance.solved_grid.itervalues()]
})

solutionDf = solutionDf[solutionDf['assignment'] == 1]
solved_table = solutionDf.pivot(index = 'i', columns = 'j', values = 'k')

print(solved_table)
