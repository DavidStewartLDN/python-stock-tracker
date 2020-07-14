# Reading from csv file created by pythin book 1

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

df = pd.read_csv('tsla.csv', parse_dates = True, index_col=0)

df['100ma'] = df['Adj Close'].rolling(window=100).mean()

# Drops any values from current dataframe that have no value - such as Not a Number (NaN)
df.dropna(inplace=True)

print(df.head())
print(df.tail())

# arguments [shape - number of rows and columns, loc - where to display graph, rowspan - number of rows, colspan - no. columns, sharex - zoom affects both graphs]
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

ax1.plot(df.index, df['Adj Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Adj Close'])

plt.show()