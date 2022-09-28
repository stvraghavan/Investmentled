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

#stocks = pd.read_csv("D:/Tilak Files/Sem-9/Stockfolio/EQUITY_L.csv")
#stocks = stocks[stocks['SERIES'] == 'EQ']
today = datetime.today()
start_date = today - timedelta(days=1825)
end_date = today
tickers = ['TCS']
df = pd.DataFrame()

df = Functions.make_data(tickers, start_date, end_date)
# for i in range(len(tickers)):
#     data = gh(symbol=tickers[i],start=start_date, end=(end_date))[['Symbol','Close']]
#     data.rename(columns={'Close':data['Symbol'][0]},inplace=True)
#     data.drop(['Symbol'], axis=1,inplace=True)
#     if i == 0:
#         df = data
#     if i != 0:
#         df = df.join(data)

df.index = pd.to_datetime(df.index)
df.sort_index(inplace=True)

#print(df.index)

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

print('The optimal model is: ARIMA{} -AIC{}'.format(parameters[index_min], aic[index_min]))
model = ARIMA(df, order=parameters[index_min])
model_fit = model.fit()
print(model_fit.summary())
y = model_fit.predict()
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index,y=df['TCS'],
            mode = 'lines',
            name = "EoD"))
fig.add_trace(go.Scatter(x=df.index,y=y,
            mode = 'lines',
            name = "Model"))
fig.show()