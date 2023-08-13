import numpy as np
import json
import argparse

from .cleaner import * 
from .optimizer import * 
from .plotter import * 
from .definitions import *


parser = argparse.ArgumentParser()
parser.add_argument('-f','--foods', nargs='*', help='List of general foods to include in the diet optimization. Listing no foods includes all foods in the dataset.')
parser.add_argument('-a', '--amino', action='store_true', help='Whether to include amino acid constraints.')
parser.add_argument('--n_sweep', type=int, default=5, help='Number of gamma values to sweep over.')
parser.add_argument('--n_plot', type=int, default=4, help='Number of superfoods to plot on radar.')
parser.add_argument('--plot_dir', type=str, default='figures/', help='Directory to save plots to.')
args = parser.parse_args()

def main():
    df = clean_data()
    if args.foods is not None:
        df = subselect_data(df, args.foods)

    # Drop name column and make name dictionary.
    df.reset_index(drop=True, inplace=True)
    names = df['name']
    df = df.drop('name', axis=1)
    name_to_idx = {v: k for k, v in names.to_dict().items()}
    print(os.path.dirname(__file__))
    with open(os.path.join(os.path.dirname(__file__),
                           'data/units.json')) as json_file:
        units = json.load(json_file)

    constraints = build_constraints_dict(lower, upper, args.amino)
    print_constraints(constraints, units)

    gamma_vals = np.logspace(-1, 2, args.n_sweep)
    cals, weights, food_count = solve_lp_sweep(df, constraints, gamma_vals, names)

    plot_sweep(cals, weights, gamma_vals, args.plot_dir)
    plot_food_count(food_count, gamma_vals, args.plot_dir)
    nutritional_radar_plot(df, 
                                   [name_to_idx[name] for name, _ in food_count.most_common(args.n_plot)], 
                                   names, args.plot_dir)

if __name__ == "__main__":
    main()
