import Functions
from datetime import date, timedelta
import pandas as pd

start_date = date.today() - timedelta(days=180)
end_date = date.today()

print(start_date,end_date)