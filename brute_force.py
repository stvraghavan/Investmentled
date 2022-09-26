import Functions
from datetime import date, timedelta
import pandas as pd
import numpy as np

start_date = date.today() - timedelta(days=180)
end_date = date.today()

stocks = Functions.get_data()

sym = stocks['SYMBOL']

sym = list(sym)

data = Functions.make_data(sym, start_date, end_date)

print(data)