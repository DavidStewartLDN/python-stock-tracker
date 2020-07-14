import datetime as dt
import matplotlib.pyplot as pyplot
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

# choose styling for plot, many other optons available
style.use('ggplot')

# start and end date of information
start = dt.datetime(2000,1,1)
end = dt.date.today()

# data frame
df = web.DataReader('TSLA', 'yahoo', start, end)
print(df.tail())