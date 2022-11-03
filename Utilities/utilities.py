import pandas as pd
import numpy as np
import Functions
from datetime import date, timedelta

data = Functions.get_50data()

sym = data['Symbol']

stocks = Functions.make_data(sym,date.today()-timedelta(days=180),date.today())

avg_ret = Functions.daily_simple_return_percent(Functions.daily_simple_return(stocks))
risk = stocks.std().rename("Volatility")

metrics = pd.DataFrame()
metrics['Average Return'] = avg_ret
metrics['Volatility'] = risk
metrics = (metrics.sort_values(by=['Average Return','Volatility'],ascending=False))

metrics.to_csv("D:/Tilak Files/Sem-9/Stockfolio/Pages/Data/Metrics.csv")