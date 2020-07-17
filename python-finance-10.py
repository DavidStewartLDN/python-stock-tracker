# preprocessing for Machine Learning
import numpy
import pandas as pd
import pickle

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