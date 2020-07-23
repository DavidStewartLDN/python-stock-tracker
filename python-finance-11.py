# preprocessing for Machine Learning
import numpy
import pandas as pd
import pickle
from Collections import Counter

# each model will per company but compared against all
def process_data_for_labels(ticker):
  hm_days = 5
  df = pd.read_csv('sp500_joined_closes.csv', index_col=0)
  tickers = df.columns.values.tolist()
  df.fillna(0, inplace=True)

  for i in range(1, hm_days+1):
    # new minus the old
    # this shifts the column ticker_{}d up by the value of i so that you compare the current
    # value to {} days from now (future price)
    df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]
  
  df.fillna(0, inplace=True)

  print(df.head())
  return tickers, df

process_data_for_labels('XOM')

# *args allows you to pass any number of arguments
def buy_sell_hold(*args):
  cols = [c for c in args]
  requirement = 0.02
  for col in cols:
    if col > requirement:
      return 1
    if col < -requirement:
      return -1
  return 0


def extract_featuresets(ticker):
  tickers, df = process_data_for_labels(ticker)

  df['{}_target'.format(ticker)] = list(map( buy_sell_hold,
                                              df['{}_1d'.format(ticker, i)],
                                              df['{}_2d'.format(ticker, i)],
                                              df['{}_3d'.format(ticker, i)],
                                              df['{}_4d'.format(ticker, i)],
                                              df['{}_5d'.format(ticker, i)],
                                              df['{}_6d'.format(ticker, i)],
                                              df['{}_7d'.format(ticker, i)]
                                              ))

  vals = df['{}_target'.format(ticker)].values.tolist()
  str_vals = [str(i) for i in vals]
  print('Data spread:', Counter(str_vals))