import bs4 as bs
# serialises any python object - save S& P 500 lsit without having to go back to wiki
import pickle
import requests

import datetime as dt
#  os can make new directories for us
import os
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

style.use('ggplot')


def save_sp500_tickers():
  resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
  soup = bs.BeautifulSoup(resp.text, 'lxml')
  table = soup.find('table', {'id':'constituents'})
  tickers = []
  for row in table.findAll('tr')[1:]:
    ticker = row.find('td').text.strip()
    if "." in ticker:
      ticker = ticker.replace('.', '-')
      print('ticker replaced to {}'.format(ticker))
    tickers.append(ticker)

  with open("sp500tickers.pickle", "wb") as f:
    pickle.dump(tickers, f)

  print("Collected ticker data")
  return tickers

def get_data_from_yahoo(reload_sp500=False):
  # saving this data locally to avoid 20/30 minute download from yahoo each iteration
  if reload_sp500:
    tickers = save_sp500_tickers()
  else:
    # wb = write bytes and rb = read bytes - ahhh!
    with open("sp500tickers.pickle", "rb") as f:
      tickers = pickle.load(f)

  # checks is path exists and if not, creates it
  if not os.path.exists('stock_dfs'):
    os.makedirs('stock_dfs')

  start = dt.datetime(2000,1,1)
  end = dt.date.today()

  # for ticker in tickers[:25]: - this would select the first 25 companies in ticker list
  for ticker in tickers:
    if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
      df = web.DataReader(ticker, 'yahoo', start, end)
      df.to_csv('stock_dfs/{}.csv'.format(ticker))
      print('Successfuly downloaded data for {} from {} to {}'.format(ticker, start, end))
    else:
      print('Already have {}'.format(ticker))

def compile_data():
  with open("sp500tickers.pickle", "rb") as f:
    tickers = pickle.load(f)
    
  main_df = pd.DataFrame()

  # enumerate let's us count things
  for count, ticker in enumerate(tickers):
    df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
    df.set_index('Date', inplace=True)

    # 'Adj close':ticker -> renames column from x to y
    df.rename(columns = {'Adj Close':ticker}, inplace=True)
    df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

    if main_df.empty:
      main_df = df
    else:
      main_df = main_df.join(df, how = 'outer')

    if count % 10 == 0:
      print(count)

  print(main_df.head())
  main_df.to_csv('sp500_joined_closes.csv')

def visualize_data(type='percent'):
  df = pd.read_csv('sp500_joined_closes.csv')
  # df['AAPL'].plot()
  # plt.show()

  # correlation table created - stock tickers onboth axises and correlation between prices of each
  if type == 'percent':
    df.set_index('Date', inplace=True) 
    df_corr = df.pct_change().corr()
  elif type == 'price':
    df_corr = df.corr()

  print(df_corr.head())

  data = df_corr.values
  fig = plt.figure()
  # one by one fig and plot number 1
  ax = fig.add_subplot(1,1,1)

  # Red, yellow to green for negative, neutral to positive
  heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
  fig.colorbar(heatmap)
  # defines ticks at every half mark
  ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
  ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
  # removes gap at top of matplot lib chart
  ax.invert_yaxis()
  # moves the x axis values from default bottom to top
  ax.xaxis.tick_top()

  column_labels = df_corr.columns
  row_labels = df_corr.index

  ax.set_xticklabels(column_labels)
  ax.set_yticklabels(row_labels)

  plt.xticks(rotation=90)
  # defines the max values (limits) of the colours
  heatmap.set_clim(-1,1)
  plt.tight_layout()
  plt.show()

# sentdex suggested to use 'price' but percent change seems like better default
visualize_data()