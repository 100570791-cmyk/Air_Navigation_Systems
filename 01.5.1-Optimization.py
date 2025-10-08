from __future__ import division
from pyomo.environ import Binary
from coopr.pyomo import *
import os

# Initialize model
model = AbstractModel()

# Number of variable xn
model.n = Param()
# Number of inequality constraints
model.m = Param()
# Establish indexes for parameters
model.N = Set()
model.M = Set()
# Coefficients imported from external data file
model.a = Param(model.M, model.N) # Inequality coefficients
model.b = Param(model.M) # Inequality RHS terms
model.c = Param(model.N) # Objective function coefficients
# the next line declares a variable indexed by the set N
model.x = Var(model.N, within=Binary) # xn >= 0
# Construct the objective function z = a1x1+a2x2+....+anxn
def obj_expression(model):
    return sum(model.c[j]*model.x[j] for j in model.N)

model.obj = Objective(rule=obj_expression, sense=minimize)
# Construct the constraints c1xc2x2+...+cnxn<=bm

def ax_constraint_rule(model, i):
# return the expression for the constraint for i
    return sum(model.a[i, j] * model.x[j] for j in model.N) <= model.b[i]

# the next line creates one constraint for each member of the set model.M
model.AxbConstraint = Constraint(model.M, rule=ax_constraint_rule)

# pyomo solve 01.5.1-Optimization.py 01.5.2-Data.dat --solver=glpk --show-results
