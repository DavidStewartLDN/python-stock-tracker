# preprocessing for Machine Learning
import numpy
import pandas as pd
import pickle

# each model will per company but compared against all
def process_data_for_labels(ticker):
  hm_days = 7
  df = pd.read_csv('sp500_joined_closes.csv', index_col=0)
  tickers = df.columns.values.tolist()
  df.fillna(0, inplace=True)

  for i in range(1, hm_days+1):
    # new minus the old
    df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]
  
  df.fillna(0, inplace=True)

  print(df.head())
  return tickers, df

process_data_for_labels('XOM')