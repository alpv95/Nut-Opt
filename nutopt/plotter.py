import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from collections import Counter
from collections.abc import Sequence

from nutopt.definitions import *


plot_dir = '../figures/'

def plot_food_count(food_count: Counter, gamma_vals):
    fig, ax = plt.subplots(figsize=(10,5))
    labels, values = zip(*food_count.most_common())

    indexes = np.arange(len(labels))
    width = 1

    ax.bar(indexes, [value / len(gamma_vals) * 100 for value in values], width)
    ax.set_xticks(indexes + width * 0.5)
    ax.set_xticklabels(labels, rotation='vertical')
    ax.set_ylabel("Appearance Fraction [%]")
    plt.savefig(os.path.join(plot_dir,'food_count.png'), format='png', dpi=300, bbox_inches="tight")

def plot_sweep(cals, weights, gamma_vals):
    # Pareto frontier
    fig, ax = plt.subplots()

    ax.plot(cals, weights)
    ax.scatter(cals, weights,)

    for idx in [0, int(len(gamma_vals) / 2), -1]:
        ax.annotate(f"$\gamma = {gamma_vals[idx]:.1f}$",xy=(cals[idx]+5, weights[idx]+30))

    ax.set_ylabel('Weight [g]')
    ax.set_xlabel('Calories [kcal]')
    plt.savefig(os.path.join(plot_dir,'pareto_frontier.png'), format='png', dpi=300, bbox_inches="tight")

def nutritional_radar_plot(df: pd.DataFrame, food_idxs: Sequence, names: dict, 
                           n_contours: int=5, ranges: list=[20,1.5,800,20,300,10]):
    fig, axs = plt.subplots(figsize=(12,12), ncols=2, nrows=3, subplot_kw=dict(polar=True), 
                        gridspec_kw={'wspace': 0.0, 'hspace': 0.5})
    axs = axs.flatten()

    for ax, group, radius in zip(axs,[summary, essential, 
                                    macro_minerals, trace_minerals, 
                                    vitamins, fatty_acids], ranges):
        ax.set_ylim(0, radius)
        ax.set_rgrids(np.linspace(0, radius, n_contours))
        
        for food_index in food_idxs:
            radar_names = df.iloc[food_index][group].index
            radar_vals = df.iloc[food_index][group].values

            label_loc = np.linspace(start=0, stop=2*np.pi, num=len(radar_names) + 1)
            radar_vals = np.append(radar_vals, radar_vals[0])
            radar_names = np.append(radar_names, radar_names[0])

            ax.plot(label_loc, radar_vals, lw=2, label=names[food_index])
            ax.fill(label_loc, radar_vals, alpha=0.3)

            _, _ = ax.set_thetagrids(np.degrees(label_loc), labels=radar_names)
        
        ax.tick_params(axis='both', which='major', pad=10, labelsize=10)

            
    ax.legend(loc='upper left', bbox_to_anchor=(0.63,1.4))
    plt.savefig(os.path.join(plot_dir,'radar.png'), format='png', dpi=300, bbox_inches="tight")