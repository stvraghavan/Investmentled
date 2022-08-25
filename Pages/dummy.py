import streamlit as st

col1, col2= st.columns([3,1])

with col1:
    stocks = st.text_input("Enter the list of stocks you want")
    tickers = stocks.split(",")
    print(type(tickers))