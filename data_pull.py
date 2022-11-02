import pandas as pd
import gspread as gs
import datetime as dt
import pandas_datareader as web

import pandas_datareader as web

gc = gs.service_account(filename='testdashboard1-be5a120e4282.json')
sheet1 = gc.open("LITGTransaction")

ws = sheet1.worksheet('LITGTrans')
df = pd.DataFrame(ws.get_all_records())


dat = pd.DataFrame()

for n in df.iloc:
    dat[n.ticker] = web.DataReader(n.ticker, "yahoo", n.date, dt.date.today())['Close']*n.quantity

dat['Sum'] = dat[list(dat.columns)].sum(axis=1) 
dat['Cash'] = 156054.73
dat["FundValue"] = dat['Sum']+dat['Cash']

dat["FundValue"].to_csv("holdings_data.csv")




