import Functions
from datetime import date, timedelta
import pandas as pd

start_date = date.today() - timedelta(days=180)
end_date = date.today()

tickers = pd.DataFrame()

tickers = Functions.get_data()

dataframe = pd.DataFrame()

dataframe = Functions.make_data(tickers,startdate=start_date,end_date=end_date)

dsr = []

dsr = Functions.daily_simple_return(dataframe)

print(dsr.sort_values())