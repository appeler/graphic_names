#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Stratified random sample male/female first name')
    parser.add_argument('input', help='Input file name')
    parser.add_argument('-o', '--output', default='output.csv',
                        help='Output CSV file name')
    parser.add_argument('-c', '--count', type=int, default=100,
                        help='Number of name to sample')
    parser.add_argument('-m', '--min-len', type=int, default=5,
                        help='Mininum name length')
    parser.add_argument('-t', '--type', default='state',
                        help='Politician Type (all, state, local)')
    parser.add_argument('--no-header', dest='header', action='store_false',
                        help='Output without header at the first row')
    parser.set_defaults(header=True)

    args = parser.parse_args()

    print(args)

    ptype = args.type
    count = args.count
    minlen = args.min_len

    sample_names = []
    unique_names = set()
    df = pd.read_csv(args.input, usecols=['type', 'politician_name', 'gender'])
    for gender in ['male', 'female']:
        names = set()
        while True:
            gen_df = df[(df.type == ptype) & (df.gender == gender)].sample(count)['politician_name']
            gen_list = gen_df.tolist()
            for n in gen_list:
                a = n.strip().split()[0].upper()
                # Filter out name with symbol
                if len(a) < 5 or a.find('.') != -1 or a.find(',') != -1 or a.find('/') != -1:
                    continue
                if (a not in names) and (a not in unique_names):
                    names.add(a)
                    unique_names.add(a)
            if len(names) > count/2:
                break
        g = 'M' if gender == 'male' else 'F'
        sample_names.extend([(g, n) for n in list(names)[:count/2]])
    df = pd.DataFrame(sample_names, columns=['gender', 'name'])
    df.sort_values(['gender', 'name'], inplace=True)
    df.reset_index(inplace=True, drop=True)
    df.to_csv(args.output, index_label='id', header=args.header)
