import pandas as pd
import numpy as np
from nsepy import get_history as gh

def get_data():
    symbols = pd.read_csv("Data\EQUITY_L.csv")
    return symbols

def make_data(stocksymbols):
    data_frame = pd.DataFrame()
    for i in range(len(stocksymbols)):
        data = gh(symbol=stocksymbols[i],start=startdate, end=(end_date))[['Symbol','Close']]
        data.rename(columns={'Close':data['Symbol'][0]},inplace=True)
        data.drop(['Symbol'], axis=1,inplace=True)
        if i == 0:
            df = data
        if i != 0:
            df = df.join(data)
    return data_frame

def daily_simple_return(data_frame):
    dsr = data_frame.pct_change(1)
    dsr.dropna(inplace=True)
    return dsr

