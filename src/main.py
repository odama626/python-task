import argparse
import sys
import pandas as pd
import json
from pandas.io.json import json_normalize
import numpy as np

# A simple list of regex statements to remove bad names
removal = [r'^\W.*$', r'^\$.*$', r'^.*to\s.*of.*$', r'^[\s\d]+$', r'^\(.*\)$', r'^(A|The)\s.*$']

def main(args=None):
  with open(args.input_file) as json_file:
    # load json data and normalize on cast names
    json_data = json.load(json_file)
    data = json_normalize(data=json_data, record_path='cast', meta=['title', 'genres', 'year'])
    data.rename(columns={ 0: 'cast'}, inplace=True)

    # remove records with invalid cast names
    if args.cleanup:
      data['cast'].replace(regex=removal, value=np.nan, inplace=True)
      data.dropna(subset=['cast'], inplace=True)

    # sort by and group by cast and year and get the title count for each group
    results = data.sort_values(by=['cast', 'year']).groupby(['cast', 'year']).size()
    results = results.reset_index()

    # rename the new group count column to movies
    results.rename(columns={ 0: 'movies'}, inplace=True)

    with pd.option_context('display.max_rows', None):
      print(results.to_csv(index=False, sep=args.sep))



if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='JSON Data parser')
  parser.add_argument('input_file',
                      metavar='file',
                      type=str,
                      help='The path to the input file')
  parser.add_argument('-s', '--separator',
                      type=str,
                      dest='sep',
                      default=',',
                      help='The column separator to use for std output')
  parser.add_argument('-c', '--cleanup',
                      action='store_true',
                      help='Whether invalid cast names should be removed'
                      )
  main(parser.parse_args())
