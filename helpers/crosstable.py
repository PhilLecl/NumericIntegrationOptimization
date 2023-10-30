import json
import argparse
import matplotlib.pyplot as plt
import logging
import sys
import pandas as pd
import seaborn as sns


def generate_crosstable(runs: list[str], prop: str, group_by: str, color_scale: str,
                        outpath: str):
    data = pd.DataFrame()
    for run in runs:
        with open(run) as f:
            run_json = json.load(f)
        for test in run_json['benchmarks']:
            row = pd.DataFrame(
                [{'run': run, 'group': test[group_by], 'value': float(test['stats'][prop])}])
            data = pd.concat([data, row], ignore_index=True)
    data['nval'] = data.apply(lambda r: r.value/ data[data.group == r.group].value.min(), axis=1)
    data = data.pivot(columns='run', index='group', values='nval')
    print(data)
    sns.heatmap(data, annot=True)
    plt.savefig(outpath)
    plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Crosstable Generator',
        description='Generates a crosstable of pytest-benchmark runs',
    )
    parser.add_argument('-g', '--group-by', default='name')
    parser.add_argument('-c', '--color-scale', default='log')
    parser.add_argument('-p', '--property', default='mean')
    parser.add_argument('-o', '--output', default='crosstable.svg')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('benchmarks', nargs='+')
    args = parser.parse_args()
    logging.basicConfig(level=min(10, 40 - 10 * args.verbose))
    generate_crosstable(args.benchmarks, args.property, args.group_by, args.color_scale,
                        args.output)
