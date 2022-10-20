import Functions
from datetime import date, timedelta
import pandas as pd
import numpy as np

start_date = date.today() - timedelta(days=180)
end_date = date.today()

stocks = Functions.get_data()

sym = stocks['Symbol']

sym = list(sym)

dataframe = Functions.make_data(sym,startdate=start_date,end_date=end_date)

avg_ret = Functions.daily_simple_return(dataframe)

print(type(avg_ret))
print(avg_ret.sort_values(ascending=False))
