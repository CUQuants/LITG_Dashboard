import datetime as dt
import pandas as pd

import pandas_datareader as web



# end_date = dt.date.today()
# start_date = dt.date(end_date.year - 1, end_date.month, end_date.day)

tickers = ["ABB", "AAPL", "BLK", "DFS", "EOG", "HD", "JPM", "KGC", "MBUU", "MCD", "MDT", "MSFT", "NVDA", "PTC", "REGN", "SE", "SRE", "SOFI", "UNH", "VLD"]

df = web.DataReader(tickers, "yahoo", '2022-01-01', '2022-10-08')['Close']
df.to_csv("holdings_data.csv")



# import datetime as dt
# import pandas_datareader as web

# end_date = dt.date.today()
# start_date = dt.date(end_date.year - 50, end_date.month, end_date.day)

# tickers = ["DGS3MO", "DGS2", "DGS10", "T10Y2Y"]
# df = web.DataReader(tickers, "fred", start_date, end_date).dropna()
# df.to_csv("yield_curve_data.csv")