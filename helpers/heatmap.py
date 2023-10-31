#! /bin/env python3

import json
import argparse
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
import logging
import sys
import pandas as pd
import seaborn as sns
import os
from sklearn.preprocessing import minmax_scale


def generate_heatmap(runs: list[str], prop: str, group_by: str, color_scale: str, normalize: bool,
                     individual_groups: bool, outpath: str):
    data = pd.DataFrame()
    for run in runs:
        with open(run) as f:
            run_json = json.load(f)
        for test in run_json['benchmarks']:
            row = pd.DataFrame(
                [{'run': os.path.split(run)[1][:4], 'test': test[group_by],
                  'value': float(test['stats'][prop])}])
            data = pd.concat([data, row], ignore_index=True)
    data = data.pivot(index='test', columns='run', values='value')
    data.loc['sum'] = data.sum(axis=0)
    if normalize:
        data = data.apply(lambda x: x / x.min(), axis=1)

    if individual_groups:
        sdata = data.copy(deep=True)
        sdata.loc[:, :] = minmax_scale(sdata, axis=1)
    else:
        sdata = data

    match color_scale:
        case 'lin' | 'linear':
            norm = Normalize()
        case _:
            norm = LogNorm()

    sns.heatmap(sdata, annot=data, cbar=(not individual_groups), norm=norm,
                cmap=sns.color_palette('rocket_r', as_cmap=True),
                xticklabels=1, yticklabels=1)
    plt.savefig(outpath, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Crosstable Generator',
        description='Generates a performance heatmap of pytest-benchmark runs',
    )
    parser.add_argument('-g', '--group-by', default='name')
    parser.add_argument('-c', '--color-scale', default='log')
    parser.add_argument('-p', '--property', default='mean')
    parser.add_argument('-a', '--absolute_values', action='store_true')
    parser.add_argument('-i', '--individual_groups', action='store_true')
    parser.add_argument('-o', '--output', default='heatmap.svg')
    # parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('benchmarks', nargs='+')
    args = parser.parse_args()
    generate_heatmap(args.benchmarks, args.property, args.group_by, args.color_scale,
                     (not args.absolute_values), args.individual_groups, args.output)
