import pandas as pd
import numpy as np
<<<<<<< HEAD
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
=======
import pandas as pd
import Functions
from datetime import date,timedelta
import plotly.graph_objects as go
import streamlit as st

stocks = ['M&M','TCS','INFY']

tickers = st.selectbox("Select the stock",options=stocks)

data = Functions.make_all_data(tickers,date.today()-timedelta(days=180),date.today())

data.index = pd.to_datetime(data.index)

st.write(data)
>>>>>>> 8bdaa34e196263023f9e7eb9b68e175511a2c3ea
