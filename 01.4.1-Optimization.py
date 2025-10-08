from __future__ import division
from pyomo.environ import Binary, NonNegativeReals
from coopr.pyomo import *
import os


# Initialize model
model = AbstractModel()

# Number of variable xn
model.n_x = Param()
model.n_y = Param()

# Number of inequality constraints
model.m = Param()

# Establish indexes for parameters
model.N_x = Set()
model.N_y = Set()
model.M = Set()

# Coefficients imported from external data file
model.a = Param(model.M, model.N_x | model.N_y) # Inequality coefficients
model.b = Param(model.M) # Inequality RHS terms
model.c = Param(model.N_x | model.N_y) # Objective function coefficients

# the next line declares a variable indexed by the set N
model.x = Var(model.N_x, within=NonNegativeIntegers) # xn >= 0
model.y = Var(model.N_y, within=Binary)


# Construct the objective function z = a1x1+a2x2+....+anxn
def obj_expression(model):
    return sum(model.c[j]*model.x[j] for j in model.N_x) + sum(model.c[j]*model.y[j] for j in model.N_y)
model.obj = Objective(rule=obj_expression, sense=minimize)

# Construct the constraints c1xc2x2+...+cnxn<=bm
def ax_constraint_rule(model, i):
    # return the expression for the constraint for i
    return sum(model.a[i, j] * model.x[j] for j in model.N_x) + sum(model.a[i, j] * model.y[j] for j in model.N_y) >= model.b[i]

# the next line creates one constraint for each member of the set model.M
model.AxbConstraint = Constraint(model.M, rule=ax_constraint_rule)

# pyomo solve 01.4.1-Optimization.py 01.4.2-Data.dat --solver=glpk --show-results
