import bs4 as bs
# serialises any python object - save S& P 500 lsit without having to go back to wiki
import pickle
import requests

import datetime as dt
#  os can make new directories for us
import os
import pandas as pd
import pandas_datareader.data as web


def save_sp500_tickers():
  resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
  soup = bs.BeautifulSoup(resp.text, 'lxml')
  table = soup.find('table', {'id':'constituents'})
  tickers = []
  for row in table.findAll('tr')[1:]:
    ticker = row.find('td').text.strip()
    tickers.append(ticker)

  with open("sp500tickers.pickle", "wb") as f:
    pickle.dump(tickers, f)

  return tickers

def get_data_from_yahoo(reload_sp500=False):
  # saving this data locally to avoid 20/30 minute download from yahoo each iteration
  if reload_sp500:
    tickers = save_sp500_tickers()
  else:
    # wb = write bites and rb = read bites - ahhh!
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


get_data_from_yahoo()

def get_sp500_ticker_data():
  tickers = save_sp500_tickers()

  for ticker in tickers:
    print(ticker)
    df = web.DataReader(ticker, 'yahoo', start, end)
    print(df.tail())

get_sp500_ticker_data()