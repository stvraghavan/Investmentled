from tracemalloc import start
import pandas as pd
import numpy as np
import math
from sklearn.metrics import mean_squared_error
from numpy import array
from datetime import datetime , timedelta 
from nsepy import get_history as gh
import matplotlib as plt
import itertools
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from tqdm import tqdm
import warnings
import plotly.graph_objects as go
import Functions
#import streamlit as st

today = datetime.today()
start_date = today - timedelta(days=1825)
end_date = today
data = Functions.get_all_data()
#tickers = st.selectbox("Select the stock symbol",data['Symbol'])
tickers = ['TCS']
df = pd.DataFrame()

df = Functions.make_data(tickers, start_date, end_date)
df.index = pd.to_datetime(df.index)
df.sort_index(inplace=True)

# Define the p, d and q parameters to take any value between 0 and 3
p = d = q = range(0, 3)
# Generate all different combinations of p, q and q
pdq = list(itertools.product(p, d, q))

aic= []
parameters = []
for param in tqdm(pdq):
  #for param in pdq:
      try:
          warnings.filterwarnings("ignore")
          mod = sm.tsa.statespace.SARIMAX(df, order=param,enforce_stationarity=True, enforce_invertibility=True)
          results = mod.fit(disp=False)
          # save results in lists
          aic.append(results.aic)
          parameters.append(param)
          #seasonal_param.append(param_seasonal)
          # print('ARIMA{} - AIC:{}'.format(param, results.aic))
      except:
          continue
# find lowest aic          
index_min = min(range(len(aic)), key=aic.__getitem__)           

# print('The optimal model is: ARIMA{} -AIC{}'.format(parameters[index_min], aic[index_min]))
model = ARIMA(df, order=parameters[index_min])
model_fit = model.fit()
# print(model_fit.summary())
<<<<<<< HEAD
y = model_fit.predict(start=1825,end=1855)
=======
y = model_fit.predict(start=len(df),end=len(df)+30)
>>>>>>> 3087d8d2875028fe82d077c2f8888074ceb653b8
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index,y=df['TCS'],
            mode = 'lines',
            name = "EoD"))
fig.add_trace(go.Scatter(x=df.index,y=y,
            mode = 'lines',
            name = "Model"))
fig.show()