from Functions import make_data,get_data,daily_simple_return
from datetime import date, timedelta
import pandas as pd

start_date = date.today() - timedelta(days=180)
end_date = date.today()

tickers = pd.DataFrame()

tickers = get_data()

dataframe = pd.DataFrame()

dataframe = make_data(tickers,startdate=start_date,end_date=end_date)

dsr = []

dsr = daily_simple_return(dataframe)

print(dsr.sort_values())