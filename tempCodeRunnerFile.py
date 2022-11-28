for n in df.iloc:
#     totalFundValue[n.ticker] = web.DataReader(n.ticker, "yahoo", n.date, dt.date.today())['Close']*n.quantity

# # for n in df.iloc:
# #     if n.action == "BUY":
# #         totalFundValue[n.ticker] = web.DataReader(n.ticker, "yahoo", n.date, dt.date.today())['Close']*n.quantity
# #         totalFundValue['Cash'] = totalFundValue['Cash'] - totalFundValue[n.ticker]
        
# #     elif n.action == "SELL":
# #         totalFundValue['Cash'] = totalFundValue['Cash'] + web.DataReader(n.ticker, "yahoo", n.date, dt.date.today())['Close']*n.quantity
# #         del df[n.ticker] #I dont think this line is necessary since Im not adding this specific column to the data frame in the first place

    

# totalFundValue['Sum'] = totalFundValue[list(totalFundValue.columns)].sum(axis=1) 

# totalFundValue["FundValue"] = totalFundValue['Sum']+totalFundValue['Cash']

# totalFundValue["FundValue"].to_csv("holdings_data.csv")