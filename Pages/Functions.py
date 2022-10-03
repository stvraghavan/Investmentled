import pandas as pd
import numpy as np
from nsepy import get_history as gh
from tqdm import tqdm

def get_50data():
    symbols = pd.read_csv("D:/Tilak Files/Sem-9/Stockfolio/ind_nifty50list.csv")
    return symbols

def get_all_data():
    symbols = pd.read_csv("D:/Tilak Files/Sem-9/Stockfolio/EQUITY_L.csv")
    return symbols

def make_data(stocksymbols,startdate,end_date):
    data_frame = pd.DataFrame()
    for i in tqdm(range(len(stocksymbols))):
        try:
            data = gh(symbol=stocksymbols[i],start=startdate, end=(end_date))[['Symbol','Close']]
            data.rename(columns={'Close':data['Symbol'][0]},inplace=True)
            data.drop(['Symbol'], axis=1,inplace=True)
            if i == 0:
                data_frame = data
            if i != 0:
                data_frame = data_frame.join(data)
        except:
            pass
    return data_frame

def daily_simple_return(data_frame):
    dsr = data_frame.pct_change(1)
    dsr.dropna(inplace=True)
    Avg_daily = dsr.mean().rename('Average Return')
    Avg_daily = Avg_daily*100
    # Avg_daily = list(Avg_daily)
    return Avg_daily