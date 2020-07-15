# Reading from csv file created by pythin book 1

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
# import mplfinance as mpf
from mplfinance.original_flavor import candlestick_ohlc
# matplot lib does not use dtae time dates - not unix time, so need to import
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web

df = pd.read_csv('tsla.csv', parse_dates = True, index_col=0)

# resample for 10 days with open high, low, close
df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

# Make dates into a column
df_ohlc.reset_index(inplace=True)
# done to convert to matplotlib date structure
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

# get all data frame values
# df.values()

print(df_ohlc.head())

# arguments [shape - number of rows and columns, loc - where to display graph, rowspan - number of rows, colspan - no. columns, sharex - zoom affects both graphs]
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
# convert dates to readable
ax1.xaxis_date()

# axis, data, thickness of candlestick, colorup - define increase col,
candlestick_ohlc(ax1, df_ohlc.values, width = 2, colorup='g')
# it will fill from 0 to the y value
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

plt.show()