import pandas as pd
import gspread as gs
import datetime as dt
import pandas_datareader as web
import numpy as np



import pandas as pd
import gspread as gs
from datetime import datetime as dt
import pandas_datareader as web
import numpy as np
import matplotlib.pyplot as plt

gc = gs.service_account(filename='testdashboard1-be5a120e4282.json')
sheet1 = gc.open("LITGTransaction")

ws = sheet1.worksheet('LITGTrans')
df = pd.DataFrame(ws.get_all_records())

df['date'] = pd.to_datetime(df['date'])
sorted_df = df.sort_values(by="date").reset_index()

f_date = np.min(sorted_df.date) # initial date
e_date = dt.now()
num_days = (e_date - f_date).days + 1

tickers = df.ticker.unique()
price_data = web.DataReader(tickers, "yahoo", f_date, dt.now())['Close']
fund_df = pd.DataFrame()

for n in tickers:
    ticker_holdings = np.zeros(num_days)
    for q in df[df.ticker == n].iloc:
        day = (q.date - f_date).days
        if q.action == "BUY":
            ticker_holdings[day] += q.quantity
        else:
            ticker_holdings[day] -= q.quantity
    for i in np.arange(1, num_days):
        ticker_holdings[i] = ticker_holdings[i - 1] + ticker_holdings[i]
    c = 0
    for date, price in zip(price_data[n].index, price_data[n]):
        day = (date - f_date).days
        while(c < num_days and c <= day):
            ticker_holdings[c] *= price
            c += 1
    fund_df[n] = ticker_holdings

fund_df.index = pd.date_range(start=f_date, end=e_date)

cash_value = np.zeros(num_days)
initial_cash = 156054.73
cash_value[0] = initial_cash

for n in sorted_df.iloc:
    day = (n.date - f_date).days
    if n.action == "BUY":
        cash_value[day] -= n.quantity * n.price
    else:
        cash_value[day] += n.quantity * n.price

for i in np.arange(1, num_days):
    cash_value[i] = cash_value[i - 1] + cash_value[i]

fund_df['Cash']=cash_value.tolist()
fund_df['Fund_Value']=fund_df[list(fund_df.columns)].sum(axis=1)

fund_df['Fund_Value'].to_csv("holdings_data.csv")

sectors = pd.DataFrame()
tmt_df=df[df.sector=="TMT"]
industrials_df=df[df.sector=="INDUSTRIALS"]
healthcare_df=df[df.sector=="HEALTHCARE"]
energy_df=df[df.sector=="ENERGY"]
financial_df=df[df.sector=="FINANCIAL"]
consumer_df=df[df.sector=="CONSUMER"]

tmt_tickers = tmt_df.ticker.unique()
industrials_tickers = industrials_df.ticker.unique()
healthcare_tickers = healthcare_df.ticker.unique()
energy_tickers = energy_df.ticker.unique()
financial_tickers = financial_df.ticker.unique()
consumer_tickers = consumer_df.ticker.unique()

sectors['TMTSum'] = fund_df[tmt_tickers].sum(axis=1)
sectors['IndustrialsSum'] = fund_df[industrials_tickers].sum(axis=1)
sectors['HealthcareSum'] = fund_df[healthcare_tickers].sum(axis=1)
sectors['EnergySum'] = fund_df[energy_tickers].sum(axis=1)
sectors['FinancialSum'] = fund_df[financial_tickers].sum(axis=1)
sectors['ConsumerSum'] = fund_df[consumer_tickers].sum(axis=1)

sectors.iloc[-1:].to_csv("sectors.csv")

# Problem, dt includes weekends

# make note to make sure lambda function doesn't run on weekends

# Another problem is initial cash for each sector will be different, but an idea is to manually go through statements and figure out what the starting cash right before each sector, or maybe even do it with no cash for the sector specific ones

#### TMT SECTOR #####
tmti_date = np.min(tmt_df.date) # initial date
tmte_date = dt.now()
tmtnum_days = (tmte_date - tmti_date).days + 1
tmt_price_data = web.DataReader(tmt_tickers, "yahoo", tmti_date, dt.now())['Close']
tmt_fund_df = pd.DataFrame()

for n in tmt_tickers:
    ticker_holdings = np.zeros(tmtnum_days)
    for q in tmt_df[tmt_df.ticker == n].iloc:
        day = (q.date - tmti_date).days
        if q.action == "BUY":
            ticker_holdings[day] += q.quantity
        else:
            ticker_holdings[day] -= q.quantity
    for i in np.arange(1, tmtnum_days):
        ticker_holdings[i] = ticker_holdings[i - 1] + ticker_holdings[i]
    c = 0
    for date, price in zip(tmt_price_data[n].index, tmt_price_data[n]):
        day = (date - tmti_date).days
        while(c < num_days and c <= day):
            ticker_holdings[c] *= price
            c += 1
    tmt_fund_df[n] = ticker_holdings

tmt_fund_df.index = pd.date_range(start=tmti_date, end=tmte_date)

tmt_fund_df['TMT_Fund_Value']=tmt_fund_df[list(tmt_fund_df.columns)].sum(axis=1)

tmt_fund_df['TMT_Fund_Value'].to_csv("tmt_holdings_data.csv")

tmt_fund_df.iloc[-1:,:-1].to_csv("tmt_pie.csv")
