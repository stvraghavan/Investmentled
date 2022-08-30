import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from nsepy import get_history as gh
from datetime import date
import pandas as pd
import numpy as np
plt.style.use('fivethirtyeight') #setting matplotlib style

user_data = st.text_input("Enter the stock symbols you want",placeholder="Please seperate the stocks with a comma (,)")
tickers = user_data.split(",")
stocksymbols = tickers
#stocksymbols = ['IRCTC']
startdate = date(2019,10,14)
end_date = date.today()
#st.write(end_date)
st.write(f"You have {len(stocksymbols)} assets in your porfolio" )

df = pd.DataFrame()
for i in range(len(stocksymbols)):
    data = gh(symbol=stocksymbols[i],start=startdate, end=(end_date))[['Symbol','Close']]
    data.rename(columns={'Close':data['Symbol'][0]},inplace=True)
    data.drop(['Symbol'], axis=1,inplace=True)
    if i == 0:
        df = data
    if i != 0:
        df = df.join(data)
#df
#df = df.sort_index()\
df = df.rename(index={"Date"})
fig, ax = plt.subplots(figsize=(15,8))
for i in df.columns.values :
    ax.plot(df[i], label = i)
ax.set_title("Portfolio Close Price History")
ax.set_xlabel('Date', fontsize=18)
ax.set_ylabel('Close Price INR (Rs)' , fontsize=18)
ax.legend(df.columns.values , loc = 'upper left')
st.pyplot(fig)
#lables = [x for i in range(df.columns.values)]
#df = df.reindex("Date")
st.write(df.info())
print(df.index)
figure = px.line(data_frame=df,title="Portfolio Close Price History",labels=dict(x="Date",y="Close Price in INR"))
st.plotly_chart(figure)