import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from nsepy import get_history as gh
from datetime import date
import pandas as pd
import numpy as np
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