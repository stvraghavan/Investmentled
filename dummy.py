import pandas as pd
import numpy as np
import plotly.express as px
import Functions
from datetime import date, timedelta

stocksymbols = Functions.get_50data()

stocksymbols = stocksymbols['Symbol']

# print(stocksymbols)

startdate = date.today() - timedelta(days=180)
end_date = date.today()

data = Functions.make_data(stocksymbols, startdate, end_date)

# print(data)

daily_simple_return = Functions.daily_simple_return(data)

# print(daily_simple_return)

fig = px.line(daily_simple_return)
fig.update_layout(dict={
    
})
fig.show()