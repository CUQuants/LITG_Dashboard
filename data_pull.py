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
initial_cash = 300000
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

#### Industrials SECTOR #####
ind_date = np.min(industrials_df.date) # initial date
inde_date = dt.now()
indnum_days = (inde_date - ind_date).days + 1
ind_price_data = web.DataReader(industrials_tickers, "yahoo", ind_date, dt.now())['Close']
ind_fund_df = pd.DataFrame()

for n in industrials_tickers:
    ticker_holdings = np.zeros(indnum_days)
    for q in industrials_df[industrials_df.ticker == n].iloc:
        day = (q.date - ind_date).days
        if q.action == "BUY":
            ticker_holdings[day] += q.quantity
        else:
            ticker_holdings[day] -= q.quantity
    for i in np.arange(1, indnum_days):
        ticker_holdings[i] = ticker_holdings[i - 1] + ticker_holdings[i]
    c = 0
    for date, price in zip(ind_price_data[n].index, ind_price_data[n]):
        day = (date - ind_date).days
        while(c < num_days and c <= day):
            ticker_holdings[c] *= price
            c += 1
    ind_fund_df[n] = ticker_holdings

ind_fund_df.index = pd.date_range(start=ind_date, end=inde_date)

ind_fund_df['Industrials_Fund_Value']=ind_fund_df[list(ind_fund_df.columns)].sum(axis=1)

ind_fund_df['Industrials_Fund_Value'].to_csv("industrials_holdings_data.csv")

ind_fund_df.iloc[-1:,:-1].to_csv("industrials_pie.csv")

#### Healthcare SECTOR #####
hci_date = np.min(healthcare_df.date) # initial date
hce_date = dt.now()
hcnum_days = (hce_date - hci_date).days + 1
hc_price_data = web.DataReader(healthcare_tickers, "yahoo", hci_date, dt.now())['Close']
hc_fund_df = pd.DataFrame()
 
for n in healthcare_tickers:
   ticker_holdings = np.zeros(hcnum_days)
   for q in healthcare_df[healthcare_df.ticker == n].iloc:
       day = (q.date - hci_date).days
       if q.action == "BUY":
           ticker_holdings[day] += q.quantity
       else:
           ticker_holdings[day] -= q.quantity
   for i in np.arange(1, hcnum_days):
       ticker_holdings[i] = ticker_holdings[i - 1] + ticker_holdings[i]
   c = 0
   for date, price in zip(hc_price_data[n].index, hc_price_data[n]):
       day = (date - hci_date).days
       while(c < num_days and c <= day):
           ticker_holdings[c] *= price
           c += 1
   hc_fund_df[n] = ticker_holdings
 
hc_fund_df.index = pd.date_range(start=hci_date, end=hce_date)
 
hc_fund_df['Healthcare_Fund_Value']=hc_fund_df[list(hc_fund_df.columns)].sum(axis=1)
 
hc_fund_df['Healthcare_Fund_Value'].to_csv("healthcare_holdings_data.csv")
 
hc_fund_df.iloc[-1:,:-1].to_csv("healthcare_pie.csv")


#### Energy SECTOR #####
eni_date = np.min(energy_df.date) # initial date
ene_date = dt.now()
ennum_days = (ene_date - eni_date).days + 1
energy_price_data = web.DataReader(energy_tickers, "yahoo", eni_date, dt.now())['Close']
energy_fund_df = pd.DataFrame()

for n in energy_tickers:
    ticker_holdings = np.zeros(ennum_days)
    for q in energy_df[energy_df.ticker == n].iloc:
        day = (q.date - eni_date).days
        if q.action == "BUY":
            ticker_holdings[day] += q.quantity
        else:
            ticker_holdings[day] -= q.quantity
    for i in np.arange(1, ennum_days):
        ticker_holdings[i] = ticker_holdings[i - 1] + ticker_holdings[i]
    c = 0
    for date, price in zip(energy_price_data[n].index, energy_price_data[n]):
        day = (date - eni_date).days
        while(c < num_days and c <= day):
            ticker_holdings[c] *= price
            c += 1
    energy_fund_df[n] = ticker_holdings

energy_fund_df.index = pd.date_range(start=eni_date, end=ene_date)

energy_fund_df['Energy_Fund_Value']=energy_fund_df[list(energy_fund_df.columns)].sum(axis=1)

energy_fund_df['Energy_Fund_Value'].to_csv("energy_holdings_data.csv")

energy_fund_df.iloc[-1:,:-1].to_csv("energy_pie.csv")

#### Financial SECTOR #####
fi_date = np.min(financial_df.date) # initial date
fe_date = dt.now()
fnum_days = (fe_date - fi_date).days + 1
fin_price_data = web.DataReader(financial_tickers, "yahoo", fi_date, dt.now())['Close']
fin_fund_df = pd.DataFrame()
 
for n in financial_tickers:
   ticker_holdings = np.zeros(fnum_days)
   for q in financial_df[financial_df.ticker == n].iloc:
       day = (q.date - fi_date).days
       if q.action == "BUY":
           ticker_holdings[day] += q.quantity
       else:
           ticker_holdings[day] -= q.quantity
   for i in np.arange(1, fnum_days):
       ticker_holdings[i] = ticker_holdings[i - 1] + ticker_holdings[i]
   c = 0
   for date, price in zip(fin_price_data[n].index, fin_price_data[n]):
       day = (date - fi_date).days
       while(c < num_days and c <= day):
           ticker_holdings[c] *= price
           c += 1
   fin_fund_df[n] = ticker_holdings
 
fin_fund_df.index = pd.date_range(start=fi_date, end=fe_date)
 
fin_fund_df['Financial_Fund_Value']=fin_fund_df[list(fin_fund_df.columns)].sum(axis=1)
 
fin_fund_df['Financial_Fund_Value'].to_csv("financial_holdings_data.csv")
 
fin_fund_df.iloc[-1:,:-1].to_csv("financial_pie.csv")

#### Consumer SECTOR #####
cons_idate = np.min(consumer_df.date) # initial date
cons_edate = dt.now()
cons_days = (cons_edate - cons_idate).days + 1
cons_price_data = web.DataReader(consumer_tickers, "yahoo", cons_idate, dt.now())['Close']
cons_fund_df = pd.DataFrame()
 
for n in consumer_tickers:
   ticker_holdings = np.zeros(cons_days)
   for q in consumer_df[consumer_df.ticker == n].iloc:
       day = (q.date - cons_idate).days
       if q.action == "BUY":
           ticker_holdings[day] += q.quantity
       else:
           ticker_holdings[day] -= q.quantity
   for i in np.arange(1, cons_days):
       ticker_holdings[i] = ticker_holdings[i - 1] + ticker_holdings[i]
   c = 0
   for date, price in zip(cons_price_data[n].index, cons_price_data[n]):
       day = (date - cons_idate).days
       while(c < num_days and c <= day):
           ticker_holdings[c] *= price
           c += 1
   cons_fund_df[n] = ticker_holdings
 
cons_fund_df.index = pd.date_range(start=cons_idate, end=cons_edate)
 
cons_fund_df['Consumer_Fund_Value']=cons_fund_df[list(cons_fund_df.columns)].sum(axis=1)
 
cons_fund_df['Consumer_Fund_Value'].to_csv("consumer_holdings_data.csv")
 
cons_fund_df.iloc[-1:,:-1].to_csv("consumer_pie.csv")

