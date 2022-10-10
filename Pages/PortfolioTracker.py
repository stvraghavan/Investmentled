from matplotlib import ticker
from prometheus_client import Metric
import streamlit as st
import pandas as pd
import numpy as np

from datetime import date, timedelta
from nsepy import get_history as gh
import plotly.express as px

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import  risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

from Functions import make_data,get_50data,get_all_data,word_cloud,daily_simple_return,daily_simple_return_percent,get_metrics,make_all_data

st.title("Stockfolio💲💲💲")

tab1,tab2 = st.tabs(["Stock Tracker","Portfolio Optimiser"])

with tab1:
    
    with st.expander("Stock Symbols"):
        NSE_data = get_all_data()
        NSE_data = NSE_data[NSE_data['SERIES'] == 'EQ']
        st.write(NSE_data[['NAME OF COMPANY','Symbol']])
    with st.expander("Top Performing Stocks"):
        Metrics = get_metrics()
        st.write(Metrics)

        
    user_data = st.multiselect("Enter the stock symbols you want",NSE_data['Symbol'])
    stocksymbols = user_data
    #stocksymbols = ['IRCTC']
    startdate = date.today() - timedelta(days=180)
    end_date = date.today()
    #st.write(end_date)
    st.write(f"You have selected {len(stocksymbols)} stocks" )

    df = pd.DataFrame()

    df = make_data(stocksymbols, startdate, end_date)

    daily_simple_return = daily_simple_return(df)

    with st.expander("Candle Stick charts"):
        import plotly.graph_objects as go

        tickers = st.selectbox("Select the stock",options=stocksymbols)
        st_date = st.date_input("Select a starting date")
        data = make_all_data(tickers,startdate=st_date,end_date=end_date)
        data.index = pd.to_datetime(data.index)
        fig = go.Figure(data=[go.Candlestick(x=data.index,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'])])
        st.plotly_chart(fig)

    st.write('Daily simple returns')

    fig = px.line(daily_simple_return,title="Volatility in Daily simple returns")
    fig.update_layout(legend_title_text="Stocks")
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Daily Simple Returns")
    st.plotly_chart(fig)
    with st.expander("This chart depicts the earnings from the previous day"):
        st.write("Daily return is calculated by subtracting the opening price from the closing price.If you are calculating for a per-share gain, you simply multiply the result by your share amount. If you are calculating for percentages, you divide by the opening price, then multiply by 100.")


    st.write('Average Daily returns(%) of stocks in your portfolio')
    Avg_daily = daily_simple_return.mean()
    st.write((Avg_daily*100).rename("Average Daily return (in %)"))

    labels = daily_simple_return.columns
    fig = px.box(daily_simple_return,title = "Risk Box Plot")
    st.plotly_chart(fig)
    with st.expander("A Box plot to show volatility"):
        st.write("A box plot is a tool which shows the spread of data under study. This shows the central value, the extremes and their point of seperation")

    st.write('Annualized Standard Deviation (Volatality(%), 252 trading days) of individual stocks in your portfolio on the basis of daily simple returns.')
    st.write((daily_simple_return.std() * np.sqrt(252) * 100).rename("Volatility"))

    st.write((Avg_daily / (daily_simple_return.std() * np.sqrt(252)) *100).rename("Earning per unit risk"))

    daily_cummulative_simple_return = (daily_simple_return+1).cumprod()

    #visualize the daily cummulative simple return
    st.write('Cummulative Returns')

    fig = px.line(daily_cummulative_simple_return,title="Daily Cummulative Simple returns/growth of investment")
    fig.update_layout(legend_title_text="Stocks")
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Growth of Rs 1 investment")
    st.plotly_chart(fig)

    with st.expander("A chart which shows the cummulative gain seen across days"):
        st.write("The cumulative return is the total change in the investment price over a set time—an aggregate return, not to be confused with annualized return.")

with tab2:

    mean = expected_returns.mean_historical_return(df)

    S = risk_models.sample_cov(df) # for sample covariance matrix

    fig = px.imshow(S,text_auto=True)

    # sb.heatmap(S,xticklabels=S.columns, yticklabels=S.columns,
    # cmap='RdBu_r', annot=True, linewidth=0.5)
    st.write('Covariance between daily simple returns of stocks in your portfolio')
    st.plotly_chart(fig)
    with st.expander("A chart which descibes the relationship between the selected stocks"):
        st.write("Covariance is a statistical tool that is used to determine the relationship between the movements of two random variables. (Note: The covariance with the stock itself is know as variance)")
    try:
        ef = EfficientFrontier(mean,S)
        weights = ef.max_sharpe() #for maximizing the Sharpe ratio #Optimization
        cleaned_weights = ef.clean_weights() #to clean the raw weights
        # Get the Keys and store them in a list
        labels = list(cleaned_weights.keys())
        # Get the Values and store them in a list
        values = list(cleaned_weights.values())
        fig = px.pie(values=values,names=labels)
        st.write('Portfolio Allocation')
        st.plotly_chart(fig)
        with st.expander("A pie chart depicting the volume of selected stocks"):
            st.write("This pie chart shows the percentage of stocks to hold on to from the list of stocks selected.")

        #st.write(ef.portfolio_performance(verbose=True))
        portfolio_perf = ef.portfolio_performance()
        st.write("The portfolio's performance metrics are")
        st.write("The portfolio's expected return is ",round(portfolio_perf[0]*100,2),"%")
        st.write("The Annual Volatility is ",round(portfolio_perf[1]*100,2),"%")
        st.write("Sharpe Ratio is ",round(portfolio_perf[2],2))
        with st.expander("More info"):
            st.write("The Sharpe ratio compares the return of an investment with its risk.")
            st.write("Volatility is a statistical measure of the dispersion of returns for a given security or market index. In most cases, the higher the volatility, the riskier the security. Volatility is often measured from either the standard deviation or variance between returns from that same security or market index.")
            st.write("The expected return is the profit or loss that an you anticipates")

        portfolio_amount = st.number_input("Enter the amount you want to invest: ",value=10000)
        if portfolio_amount != '' :
            # Get discrete allocation of each share per stock

            latest_prices = get_latest_prices(df)
            weights = cleaned_weights
            discrete_allocation = DiscreteAllocation(weights, latest_prices , total_portfolio_value = int(portfolio_amount))
            allocation , leftover = discrete_allocation.lp_portfolio()

            discrete_allocation_list = []


            for symbol in allocation:
                discrete_allocation_list.append(allocation.get(symbol))


            portfolio_df = pd.DataFrame(columns =['Ticker' , 'Number of stocks to buy'])

            portfolio_df['Ticker'] = allocation
            portfolio_df['Number of stocks to buy'] = discrete_allocation_list
            st.write('Number of stocks to buy with the amount of Rs ' + str(portfolio_amount))
            st.write(portfolio_df)
            st.write('Funds remaining with you will be: Rs' , int(leftover))
    except:
        pass