import gspread
import pandas as pd
import datetime as dt

from gspread_dataframe import set_with_dataframe



sa = gspread.service_account(filename = "testdashboard1-be5a120e4282.json")
sheet = sa.open("total_fund")

##TOTAL##
df = pd.read_csv("holdings_data.csv")

worksheet = sheet.worksheet("FundVal")
set_with_dataframe(worksheet, df)

sc = pd.read_csv("sectors.csv")

ws = sheet.worksheet("PChart")
set_with_dataframe(ws, sc)

##FOR TMT SECTOR
tmt = pd.read_csv("tmt_holdings_data.csv")

workshee = sheet.worksheet("TMTFundVal")
set_with_dataframe(workshee, tmt)

tmtsc = pd.read_csv("tmt_pie.csv")

tsc = sheet.worksheet("TMTPieChart")
set_with_dataframe(tsc, tmtsc)

##Industrials SECTOR##
ind = pd.read_csv("industrials_holdings_data.csv")

ind_worksheet = sheet.worksheet("INDUSTRIALSFundVal")
set_with_dataframe(ind_worksheet, ind)

ind_sc = pd.read_csv("industrials_pie.csv")

ind_ws = sheet.worksheet("INDUSTRIALSPie")
set_with_dataframe(ind_ws, ind_sc)

##Healthcare SECTOR##
hc = pd.read_csv("healthcare_holdings_data.csv")

hc_worksheet = sheet.worksheet("HealthcareFundVal")
set_with_dataframe(hc_worksheet, hc)

hc_sc = pd.read_csv("healthcare_pie.csv")

hc_ws = sheet.worksheet("HealthcarePie")
set_with_dataframe(hc_ws, hc_sc)

##Energy SECTOR##
en = pd.read_csv("energy_holdings_data.csv")

en_worksheet = sheet.worksheet("EnergyFundVal")
set_with_dataframe(en_worksheet, en)

en_sc = pd.read_csv("energy_pie.csv")

en_ws = sheet.worksheet("EnergyPie")
set_with_dataframe(en_ws, en_sc)

##Financial SECTOR##
fin = pd.read_csv("financial_holdings_data.csv")

fin_worksheet = sheet.worksheet("FinancialFundVal")
set_with_dataframe(fin_worksheet, fin)

fin_sc = pd.read_csv("financial_pie.csv")

fin_ws = sheet.worksheet("FinancialPie")
set_with_dataframe(fin_ws, fin_sc)

##Consumer SECTOR##
con = pd.read_csv("consumer_holdings_data.csv")

con_worksheet = sheet.worksheet("ConsumerFundVal")
set_with_dataframe(con_worksheet, con)

con_sc = pd.read_csv("consumer_pie.csv")

con_ws = sheet.worksheet("ConsumerPie")
set_with_dataframe(con_ws, con_sc)