import pandas as pd
import gspread as gs
import datetime as dt
import pandas_datareader as web

import pandas_datareader as web

gc = gs.service_account(filename='testdashboard1-be5a120e4282.json')
sheet1 = gc.open("LITGTransaction")

ws = sheet1.worksheet('LITGTrans')
df = pd.DataFrame(ws.get_all_records())


totalFundValue = pd.DataFrame()
totalFundValue['Cash'] = 156054.73

# This is just dummy logic, idk if it will work at all but the code that was working before this was:
# for n in df.iloc:
#     totalFundValue[n.ticker] = web.DataReader(n.ticker, "yahoo", n.date, dt.date.today())['Close']*n.quantity

for n in df.iloc:
    if n.action == "BUY":
        totalFundValue[n.ticker] = web.DataReader(n.ticker, "yahoo", n.date, dt.date.today())['Close']*n.quantity
        totalFundValue['Cash'] = totalFundValue['Cash'] - totalFundValue[n.ticker]
        
    elif n.action == "SELL":
        totalFundValue['Cash'] = totalFundValue['Cash'] + web.DataReader(n.ticker, "yahoo", n.date, dt.date.today())['Close']*n.quantity
        del df[n.ticker] #I dont think this line is necessary since Im not adding this specific column to the data frame in the first place

    

totalFundValue['Sum'] = totalFundValue[list(totalFundValue.columns)].sum(axis=1) 

totalFundValue["FundValue"] = totalFundValue['Sum']+totalFundValue['Cash']

totalFundValue["FundValue"].to_csv("holdings_data.csv")

