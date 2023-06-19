import numpy as np
import json
import argparse

import nutopt.cleaner as cleaner
import nutopt.optimizer as optimizer
import nutopt.plotter as plotter
from nutopt.definitions import *


parser = argparse.ArgumentParser()
parser.add_argument('-f','--foods', nargs='*', help='List of general foods to include in the diet optimization. Listing no foods includes all foods in the dataset.')
parser.add_argument('--n_sweep', type=int, default=10, help='Number of gamma values to sweep over.')
parser.add_argument('--n_plot', type=int, default=4, help='Number of superfoods to plot on radar.')
args = parser.parse_args()

def main():
    df = cleaner.clean_data()
    if len(args.foods) != 0:
        df = cleaner.subselect_data(df, args.foods)

    # Drop name column and make name dictionary.
    names = df['name']
    df = df.drop('name', axis=1)
    name_to_idx = {v: k for k, v in names.to_dict().items()}

    with open('../data/units.json') as json_file:
        units = json.load(json_file)

    constraints = optimizer.build_constraints_dict(lower, upper)
    optimizer.print_constraints(constraints, units)

    gamma_vals = np.logspace(-1,2,args.n_sweep)
    cals, weights, food_count = optimizer.solve_lp_sweep(df, constraints, gamma_vals, names)

    plotter.plot_sweep(cals, weights, gamma_vals)
    plotter.plot_food_count(food_count, gamma_vals)
    plotter.nutritional_radar_plot(df, 
                                   [name_to_idx[name] for name, _ in zip(*food_count.most_common(args.n_plot))], 
                                   names)

if __name__ == "__main__":
    main()