#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Stratified random sample male/female first name')
    parser.add_argument('input', help='Input file name')
    parser.add_argument('-o', '--output', default='output-img-subset.csv',
                        help='Output CSV file name')
    parser.add_argument('-c', '--count', type=int, default=1500,
                        help='Number of name to sample')
    parser.add_argument('-r', '--random-state', type=int, default=None,
                        help='Random state')
    parser.add_argument('-m', '--min-url', type=int, default=200,
                        help='Mininum number of image URL')
    parser.add_argument('-s', '--start', type=int, default=0,
                        help='Start index')
    parser.add_argument('-n', '--n', type=int, default=375,
                        help='Amount of name to be subset of each gender')
    parser.add_argument('--no-header', dest='header', action='store_false',
                        help='Output without header at the first row')
    parser.set_defaults(header=True)

    args = parser.parse_args()

    print(args)

    df = pd.read_csv(args.input)

    sdf = df[['gender', 'name', 'image_url']]

    gs = sdf.groupby(['gender', 'name']).size()
    # to make sure there are valid URLs enough to tag, filter out only names
    # that more than 2*count URLs
    gs = gs[gs > args.min_url]

    gdf = gs.reset_index()

    names = []
    for gender in gdf['gender'].unique():
        xdf = gdf[gdf.gender == gender].sample(args.count/2, random_state=args.random_state)
        names.extend(xdf.name.tolist()[args.start:args.start + args.n])

    odf = df[df.name.isin(names)]
    odf.to_csv(args.output, index=False, header=args.header)
