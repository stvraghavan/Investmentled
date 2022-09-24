import pandas as pd
import numpy as np
'''from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
import tensorflow as tf
'''
import math
from sklearn.metrics import mean_squared_error
from numpy import array
from datetime import datetime
from datetime import timedelta
from nsepy import get_history as gh
import matplotlib as plt
import itertools

#stocks = pd.read_csv("D:/Tilak Files/Sem-9/Stockfolio/EQUITY_L.csv")
#stocks = stocks[stocks['SERIES'] == 'EQ']
today = datetime.today()
start_date = today - timedelta(days=1825)
end_date = today
tickers = ['TCS']
df = pd.DataFrame()

for i in range(len(tickers)):
    data = gh(symbol=tickers[i],start=start_date, end=(end_date))[['Symbol','Close']]
    data.rename(columns={'Close':data['Symbol'][0]},inplace=True)
    data.drop(['Symbol'], axis=1,inplace=True)
    if i == 0:
        df = data
    if i != 0:
        df = df.join(data)
'''df1=
scaler=MinMaxScaler(feature_range=(0,1))
df1=scaler.fit_transform(np.array(df1).reshape(-1,1))
training_size=int(len(df1)*0.65)
test_size=len(df1)-training_size
train_data,test_data=df1[0:training_size,:],df1[training_size:len(df1),:1]

def create_dataset(dataset, time_step=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-time_step-1):
		a = dataset[i:(i+time_step), 0]   ###i=0, 0,1,2,3-----99   100 
		dataX.append(a)
		dataY.append(dataset[i + time_step, 0])
	return numpy.array(dataX), numpy.array(dataY)

time_step = 100

X_train, y_train = create_dataset(train_data, time_step)
X_test, ytest = create_dataset(test_data, time_step)
X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)
X_test = X_test.reshape(X_test.shape[0],X_test.shape[1] , 1)

model=Sequential()
model.add(LSTM(50,return_sequences=True,input_shape=(100,1)))
model.add(LSTM(50,return_sequences=True))
model.add(LSTM(50))
model.add(Dense(1))

model.compile(loss='mean_squared_error',optimizer='adam')
model.fit(X_train,y_train,validation_data=(X_test,ytest),epochs=100,batch_size=64,verbose=1)

train_predict=model.predict(X_train)
test_predict=model.predict(X_test)

train_predict=scaler.inverse_transform(train_predict)
test_predict=scaler.inverse_transform(test_predict)

print(math.sqrt(mean_squared_error(y_train,train_predict)))
print(math.sqrt(mean_squared_error(ytest,test_predict)))'''
df.index = pd.to_datetime(df.index)
df.sort_index(inplace=True)

#print(df.index)
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
# Define the p, d and q parameters to take any value between 0 and 3
p = d = q = range(0, 3)
# Generate all different combinations of p, q and q
pdq = list(itertools.product(p, d, q))

aic= []
parameters = []
for param in pdq:
  #for param in pdq:
      try:
          mod = sm.tsa.statespace.SARIMAX(df, order=param,enforce_stationarity=True, enforce_invertibility=True)
         
          results = mod.fit()
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
import plotly.express as px
y = list(y)
print(len(y))
print(df.shape)
fig1 = px.line(y)
fig1.show()
fig2 = px.line(df)
fig2.show()