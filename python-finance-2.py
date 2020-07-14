# Reading from csv file created by pythin book 1

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

df = pd.read_csv('tsla.csv', parse_dates = True, index_col=0)

# print(df.head())
print(df[['Open', 'High']].head())

df['Adj Close'].plot()
plt.show()