import datetime as dt
import pandas as pd

import pandas_datareader as web


tickers = ["ABB", "AAPL", "BLK", "DFS", "EOG", "HD", "JPM", "KGC", "MBUU", "MCD", "MDT", "MSFT", "NVDA", "PTC", "REGN", "SE", "SRE", "SOFI", "UNH", "VLD"]

df = web.DataReader(tickers, "yahoo", '2022-04-25', dt.date.today())['Close']

df["Cash"] = 156054.73
df["Holdings"] = (df["ABB"]*258)+ df["AAPL"]*50+df["BLK"]*20+df["DFS"]*42+df["EOG"]*66+df["HD"]*25+df["JPM"]*56+df["KGC"]*1340+df["MBUU"]*116+df["MCD"]*94+df["MDT"]*46+df["MSFT"]*209+df["NVDA"]*40+df["PTC"]*79+df["REGN"]*6+df["SE"]*38+df["SRE"]*43+df["SOFI"]*600+df["UNH"]*14+df["VLD"]*1250

df["FundValue"]= df["Cash"]+df["Holdings"]
df["FundValue"].to_csv("holdings_data.csv")




