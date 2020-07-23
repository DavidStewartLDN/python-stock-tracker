# preprocessing for Machine Learning
import numpy as np
import pandas as pd
import pickle
from collections import Counter

hm_days = 5

# each model will per company but compared against all
def process_data_for_labels(ticker):
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
  df['{}_target'.format(ticker)] = list(map(buy_sell_hold,
                                    *[df['{}_{}d'.format(ticker, i)]for i in range(1, hm_days+1)]))

  # This gives us the distributions 
  vals = df['{}_target'.format(ticker)].values.tolist()
  str_vals = [str(i) for i in vals]
  print('Data spread:', Counter(str_vals))
  # removes na's from data set
  df.fillna(0, inplace=True)
  # removes infinite values to clean data, e.g. 
  df = df.replace([np.inf, -np.inf], np.nan)
  df.dropna(inplace=True)

  # create values for feature set and labels

  # create the values
  # if we passed all the values in df including the % change over 7 days it would use these values
  # incorrectly and classify them and use them as trend. 
  # pct_chnage normalises the values
  df_vals = df[[ticker for ticker in tickers]].pct_change()
  df_vals = df_vals.replace([np.inf, -np.inf], 0)
  df_vals.fillna(0, inplace=True)

  # Capital X is your feature set, and lower case y is your labels (target, class)
  # Feature set is thing that describes it - in our case it is percent changes daily
  X = df_vals.values
  y = df['{}_target'.format(ticker)].values

  # return feature set labels and dataframe
  return X, y, df

extract_featuresets('XOM')