import json
import argparse
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import logging
import sys
import pandas as pd
import seaborn as sns
import os


def generate_heatmap(runs: list[str], prop: str, group_by: str, color_scale: str,
                     outpath: str):
    data = pd.DataFrame()
    for run in runs:
        with open(run) as f:
            run_json = json.load(f)
        for test in run_json['benchmarks']:
            row = pd.DataFrame(
                [{'run': os.path.split(run)[1][:4], 'group': test[group_by],
                  'value': float(test['stats'][prop])}])
            data = pd.concat([data, row], ignore_index=True)
    data['nval'] = data.apply(lambda r: r.value / data[data.group == r.group].value.min(), axis=1)
    data = data.pivot(index='group', columns='run', values='nval')
    print(data)
    sns.heatmap(data, annot=True, norm=LogNorm(), cmap=sns.color_palette('rocket_r', as_cmap=True))
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
    parser.add_argument('-o', '--output', default='heatmap.svg')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('benchmarks', nargs='+')
    args = parser.parse_args()
    logging.basicConfig(level=min(10, 40 - 10 * args.verbose))
    generate_heatmap(args.benchmarks, args.property, args.group_by, args.color_scale,
                     args.output)
