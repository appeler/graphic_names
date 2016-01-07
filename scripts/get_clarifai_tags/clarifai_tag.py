#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json
import argparse
import time
import pandas as pd
from urllib import unquote

from glob import glob
from pprint import pprint
from ConfigParser import ConfigParser

import logging
logging.basicConfig(filename='ctag.log',level=logging.DEBUG)

from clarifai.client import ClarifaiApi, ApiThrottledError


def load_config(args=None):
    if args is None or isinstance(args, basestring):
        namespace = argparse.Namespace()
        if args is None:
            namespace.config = CFG_FILE
        else:
            namespace.config = args
        args = namespace
    try:
        config = ConfigParser()
        config.read(args.config)

        # Clarifai configuration
        args.clarifai_app_id = config.get('clarifai', 'app_id', '')
        args.clarifai_app_secret = config.get('clarifai', 'app_secret', '')
    except Exception as e:
        print(e)

    return args

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clarifai Tag API')
    parser.add_argument('input', help='Input file name')
    parser.add_argument('--config', default='clarifai.cfg',
                        help='Configuration file')
    parser.add_argument('-c', '--count', type=int, default=10,
                        help='Number of valid tag for each item')
    parser.add_argument('-b', '--batch', type=int, default=None,
                        help='Specify batch size')
    parser.add_argument('-o', '--output', default='output-img-tag.csv',
                        help='Output CSV file name')
    parser.add_argument('--no-header', dest='header', action='store_false',
                        help='Output without header at the first row')
    parser.set_defaults(header=True)

    args = parser.parse_args()

    args = load_config(args)

    print(args)

    if args.clarifai_app_id != '':
        clarifai_api = ClarifaiApi(app_id=args.clarifai_app_id, app_secret=args.clarifai_app_secret)
    else:
        #export CLARIFAI_APP_ID=<an_application_id_from_your_account>
        #export CLARIFAI_APP_SECRET=<an_application_secret_from_your_account>
        clarifai_api = ClarifaiApi()

    df = pd.read_csv(args.input)

    # FIXME: unquote URLs twice
    df['image_url'] = df['image_url'].apply(lambda x: unquote(unquote(x)))

    if 'clarifai_status' not in df.columns:
        df['clarifai_status'] = None
        df['predicted'] = '-'
        df['tags'] = None
        df['probs'] = None

    try:
        for gender in df['gender'].unique():
            names = df[df.gender == gender].name.unique().tolist()
            for name in names:
                urls = df[(df.gender == gender) & (df.name == name) & df.clarifai_status.isnull() & (df.image_url.str.contains('.jpg') | df.image_url.str.contains('.jpeg') | df.image_url.str.contains('.png'))][['image_order', 'image_url']].sort_values(['image_order'])['image_url'].tolist()
                count = len(df[(df.gender == gender) & (df.name == name) & (df.clarifai_status == 'OK') & (df.predicted != '-')])
                begin = 0
                print(gender, name, count, len(urls))
                while count < args.count and begin < len(urls):
                    need = args.count - count
                    if args.batch and need > args.batch:
                        need = args.batch
                    sel_urls = urls[begin:begin+need]
                    try:
                        result = clarifai_api.tag_urls(sel_urls)
                        for r in result['results']:
                            url = r['url'].encode('utf-8')
                            status = r['status_code']
                            try:
                                _id = df[(df.gender == gender) & (df.name == name) & (df.image_url == url)].index[0]
                                df.loc[_id, 'clarifai_status'] = status
                                if status == 'OK':
                                    tags = r['result']['tag']['classes']
                                    probs = r['result']['tag']['probs']
                                    msum = 0
                                    fsum = 0
                                    for t in ['man', 'men', 'boy', 'actor']:
                                        try:
                                            idx = tags.index(t)
                                            msum += probs[idx]
                                        except:
                                            pass
                                    for t in ['woman', 'women', 'girl', 'actress']:
                                        try:
                                            idx = tags.index(t)
                                            fsum += probs[idx]
                                        except:
                                            pass
                                    df.loc[_id, 'tags'] = str(tags)
                                    df.loc[_id, 'probs'] = str(probs)
                                    if msum > fsum:
                                        df.loc[_id, 'predicted'] = 'M'
                                        count += 1
                                    elif msum < fsum:
                                        df.loc[_id, 'predicted'] = 'F'
                                        count += 1
                            except Exception as e:
                                import traceback
                                traceback.print_exc()
                                print('Name: {}, URL: {}'.format(name, url))
                        begin += need
                    except ApiThrottledError as e:
                        print(e)
                        time.sleep(10)
                        continue
                    except Exception as e:
                        import traceback
                        traceback.print_exc()
                        for url in sel_urls:
                            _id = df[(df.gender == gender) & (df.name == name) & (df.image_url == url)].index[0]
                            try:
                                df.loc[_id, 'clarifai_status'] = e.msg['status_code']
                            except:
                                df.loc[_id, 'clarifai_status'] = 'ERROR'
                        begin += need
                #break
            #break
    finally:
        df.to_csv(args.output, index=False, header=args.header)