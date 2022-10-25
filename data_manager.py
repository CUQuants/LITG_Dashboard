import os
import sys
import time
import requests
import datetime as dt
import pandas_datareader as web

from termcolor import colored

class DataManager():

    def __init__(self):
        
        if self.check_internet_connection() == False:
            sys.exit()
            
        if self.check_json() == False:
            sys.exit()
            
        if self.collect_data() == False:
            sys.exit()
            
        if self.computation() == False:
            sys.exit()

    def check_internet_connection(self):
        
        url = "https://www.google.com"
        try:
            test_requests = requests.get(url, timeout = 5)
            print(colored("[INFO]", "green"), "Internet Connection Established")
            return True
        
        except:
            print(colored("[URGENT]", "red"), "Internet Connection Not Established")
            return False
        
    def check_json(self):

        cwd = os.getcwd()
        
        for i in os.listdir(cwd):
            
            file_ending = i
            file_ending = i.split(".")
            
            try:
                if(file_ending[1] == "json"):
                    print(colored("[INFO]", "green"), "JSON Found Using:",i)
                    return True
            except:
                pass
            
        print(colored("[URGENT]", "red"), "JSON Not Found")
        return False
    #need a file that checks that there is an AWS connection
    
    def collect_data(self):
        
        try:
    
            tickers = ["ABB", "AAPL", "BLK", "DFS", "EOG", "HD", "JPM", "KGC", "MBUU", "MCD", "MDT", "MSFT", "NVDA", "PTC", "REGN", "SE", "SRE", "SOFI", "UNH", "VLD"]

            self.df = web.DataReader(tickers, "yahoo", '2022-01-01', '2022-10-08')['Close']
            #calculate weighted avg
        
            print(colored("[INFO]", "green"), "Collected Data")
            return True
        
        except:
            
            print(colored("[URGENT]", "red"), "Data Could Not Be Collected")
            return False
