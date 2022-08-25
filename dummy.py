import streamlit as st
import plotly.express as px
col1, col2= st.columns([1,1])

with col1:
    stocks = st.text_input("Enter the list of stocks you want")
    tickers = stocks.split(",")
    st.write(type(tickers))
with col2:
    data = [65,25,10]
    labels = ["Positive","Neutral","Negative"]
    fig = px.pie(values = data,names = labels,title = "Dummy data",color=labels,
                color_discrete_map={
                    'Positive':'green',
                    'Neutral':'blue',
                    'Negative':'red'
                })
    st.plotly_chart(fig)