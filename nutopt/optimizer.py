import numpy as np
import pandas as pd
import cvxpy as cp
from collections import Counter
from collections.abc import Sequence


def get_constraint_vectors(constraints):
    ''' '''
    lower = []
    upper = []
    lower_idx = []
    upper_idx = []
    for k,v in constraints.items():
        if not isinstance(v[0], str):
            lower_idx.append(k)
            lower.append(v[0])
        if not isinstance(v[1], str):
            upper_idx.append(k)
            upper.append(v[1])
    return lower, upper, lower_idx, upper_idx

def build_constraints_dict(lower, upper):
    ''' '''
    constraints = {k_up: (v_low, v_up) for (k_up, v_up), (_, v_low) in zip(upper.items(), lower.items()) 
    if not (isinstance(v_low, str) and isinstance(v_up, str))}
    return constraints

def build_constraint_vectors(df: pd.DataFrame, constraints: dict):
    ''' '''
    l, u, l_idxs, u_idxs = get_constraint_vectors(constraints)

    #should be roughly 70 x 8700, i.e. A.T.
    Al = df[l_idxs].values.T
    Au = df[u_idxs].values.T
    return Al, Au, l, u

def print_constraints(constraints, units):
    ''' '''
    for k,v in constraints.items():
        upper = v[1]
        lower = v[0]
        if isinstance(v[1],str):
            upper = 'inf'
        if isinstance(v[0],str):
            lower = 0
        print(f"{lower} < {k} ({units[k].replace(' ','')}) < {upper}")

def solve_lp_sweep(df: pd.DataFrame, constraints: dict, gamma_vals: Sequence, 
                   names: dict):
    '''
    Solves optimal diet LP problem for a sweep over the tradeoff parameter gamma.
    Tradeoff between calories and weight.

    Input: Dataframe, dictionary of constraints, list of gamma values
    Output: list of calories, list of weights, Counter of foods
    '''
    n = len(df)
    ones = np.ones(n) # vector of food weights in units of 100g.
    calories = df['calories'].values
    idxs = np.array([i for i in range(n)])
    tol = 1e-6
    Al, Au, l, u = build_constraint_vectors(df, constraints)

    # Define and solve the CVXPY problem: minimizing calories and weight.
    x = cp.Variable(n)
    gamma = cp.Parameter(nonneg=True)
    prob = cp.Problem(cp.Minimize(calories @ x + gamma * ones @ x),
                    [Au @ x <= u, 
                    Al @ x >= l, x >= 0,])

    cals = []
    weights = []
    food_count = Counter()
    for i in range(len(gamma_vals)):
        gamma.value = gamma_vals[i]
        prob.solve()
        if x.value is None:
            print('Problem infeasible')
            break

        # Print result.
        print('Total calories: ', calories @ x.value, 'kcal')
        print('Total weight: ', x.value.sum() * 100, 'g')
        cals.append(calories @ x.value)
        weights.append(x.value.sum() * 100)

        result = x.value
        final_foods = pd.DataFrame([(names[food], food, val) for food, val 
                                    in zip(idxs[result > tol], result[result > tol])])
        food_count += Counter(final_foods[0].values)
        print(final_foods.sort_values(by=2,ascending=False))
    return cals, weights, food_count