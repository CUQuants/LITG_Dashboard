import gspread
import pandas as pd
import datetime as dt

from gspread_dataframe import set_with_dataframe


df = pd.read_csv("holdings_data.csv")

sa = gspread.service_account(filename = "testdashboard1-be5a120e4282.json")
sheet = sa.open("total_fund")


worksheet = sheet.worksheet("FundVal")
set_with_dataframe(worksheet, df)

sc = pd.read_csv("sectors.csv")

ws = sheet.worksheet("PChart")
set_with_dataframe(ws, sc)