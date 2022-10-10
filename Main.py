#Importing streamlit

import streamlit as st

st.title("Welcome to Stockfolio!! 💲💲💲")

st.header('Stockfolio is your destination to finding insights about stocks.')

st.markdown("""
    
        We provide a variety of services ranging from
    
        1. Stock tracking📈
        2. Sentiment analysis of news and twitter😀😍😫😔☹️😨🤯😭
        3. Portfolio optimisation🎯🐂🐻

        **We use Open-Source software to provide you with the service so it's perfectly safe and free**
        
 """)
st.write("Below are somethings that we want you to know before you proceed futher into this project.")
col1,col2 = st.columns(2)
with col1:
        with st.expander("How do we gather our data?"):
                st.write("""
                We collect data from the national stock exchange from a given start to a set end date using the nsepy Library available in python.
                We then remove the unecessary information to provide the needed data for the users.
                """)
        with st.expander("How do we suggest a stock?"):
                st.write("""
                We compute the various factors that we use a metrics for our stocks and provide you with a list of alternatives from which you can choose a stock.
                This gives you an idea of who is a market leader.
                """)
        with st.expander("Candle Stick Chart"):
                st.write("""
                A Candle stick chart is an essential tool to measure stock movement.
                This chart based on its colour, tells if the market is bullish or bearish.
                This chart provides OHLC (Open Hight Low and Close) values of a stock on a given day.
                """)
        with st.expander("How do we measure risk / volatility"):
                st.write('''
                Volatility or risk is usually measured using the standard deviation (price differences from the average stock price).
                ''')

with col2:
        with st.expander("Why Sentiment Analysis?"):
                st.write("""
                The stock market is a highly volatile entity affect by many people and people themselves are affect by social factors.
                By Performing sentiment analysis we can capture some of the sentiments they express online to gain a small insight on how they might influence the market. 
                """)
        with st.expander("What is Sharpe Ratio ?"):
                st.write("""
                The Sharpe ratio is a measure of return often used to compare the performance of investment managers by making an adjustment for risk.
                """)
        with st.expander("How do we do Portfolio Optimisation ?"):
                st.write("""
                Portfolio Optimisation is done mathematically by using something called an efficient frontier, which encompases all possible portfolio combinations.
                By using the Sharpe ratio as the base, the portfolio which has the maximum sharpe ratio is selected.
                """)
        with st.expander("Why are we open source ?"):
                st.write('''
                As an individual who faces financial constraint for many aspects of life, open-source software reduced a burden I faced whenever I needed a properitory software.
                I see developing this open-source app as a means to thank the open-source community for providing me with the software I need.
                ''')


st.caption("Remember the analysis work done here is only for gaining information, we are in no way responsible for any money you gain / lose. Investment in stocks is subject to market risks please make sure to read all documents carefully")
