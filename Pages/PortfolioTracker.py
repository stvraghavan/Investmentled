import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sb
from datetime import date, timedelta
from nsepy import get_history as gh
import plotly.express as px
plt.style.use('fivethirtyeight') #setting matplotlib style

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import  risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

from Functions import make_data,get_50data,get_all_data,word_cloud,daily_simple_return,daily_simple_return_percent

st.title("Stockfolio💲💲💲")

tab1,tab2 = st.tabs(["Stock Tracker","Portfolio Optimiser"])

with tab1:
    
    with st.expander("Stock Symbols"):
        NSE_data = pd.read_csv("D:/Tilak Files/Sem-9/Stockfolio/EQUITY_L.csv")
        NSE_data = NSE_data[NSE_data['SERIES'] == 'EQ']
        st.write(NSE_data[['NAME OF COMPANY','Symbol']])
    with st.expander("Top Performing Stocks"):
        start_date = date.today() - timedelta(days=180)
        end_date = date.today()
        stocks = get_50data()
        sym = stocks['Symbol']
        sym = list(sym)
        dataframe = make_data(sym,startdate=start_date,end_date=end_date)
        avg_ret = daily_simple_return_percent(daily_simple_return(dataframe))
        st.write(avg_ret.sort_values(ascending=False).head())

        
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

    st.write('# Daily simple returns')

    fig = px.line(daily_simple_return,title="Volatility in Daily simple returns")
    fig.update_layout(legend_title_text="Stocks")
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Daily Simple Returns")
    st.plotly_chart(fig)

    st.write('Average Daily returns(%) of stocks in your portfolio')
    Avg_daily = daily_simple_return.mean()
    st.write((Avg_daily*100).rename("Average Daily return (in %)"))

    labels = daily_simple_return.columns
    fig = px.box(daily_simple_return,title = "Risk Box Plot")
    st.plotly_chart(fig)

    st.write('Annualized Standard Deviation (Volatality(%), 252 trading days) of individual stocks in your portfolio on the basis of daily simple returns.')
    st.write((daily_simple_return.std() * np.sqrt(252) * 100).rename("Volatility"))

    st.write((Avg_daily / (daily_simple_return.std() * np.sqrt(252)) *100).rename("Earning per unit risk"))

    daily_cummulative_simple_return = (daily_simple_return+1).cumprod()

    #visualize the daily cummulative simple return
    st.write('Cummulative Returns')
    fig, ax = plt.subplots(figsize=(18,8))

    fig = px.line(daily_cummulative_simple_return,title="Daily Cummulative Simple returns/growth of investment")
    fig.update_layout(legend_title_text="Stocks")
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Growth of Rs 1 investment")
    st.plotly_chart(fig)

with tab2:

    mean = expected_returns.mean_historical_return(df)

    S = risk_models.sample_cov(df) # for sample covariance matrix

    # plt.style.use('ggplot')
    fig = px.imshow(S,text_auto=True)

    # sb.heatmap(S,xticklabels=S.columns, yticklabels=S.columns,
    # cmap='RdBu_r', annot=True, linewidth=0.5)
    st.write('Covariance between daily simple returns of stocks in your portfolio')
    st.plotly_chart(fig)

    ef = EfficientFrontier(mean,S)
    weights = ef.max_sharpe() #for maximizing the Sharpe ratio #Optimization
    cleaned_weights = ef.clean_weights() #to clean the raw weights
    # Get the Keys and store them in a list
    labels = list(cleaned_weights.keys())
    # Get the Values and store them in a list
    values = list(cleaned_weights.values())
    # fig, ax = plt.subplots()
    fig = px.pie(values=values,names=labels)
    st.write('Portfolio Allocation')
    st.plotly_chart(fig)

    #st.write(ef.portfolio_performance(verbose=True))
    portfolio_perf = ef.portfolio_performance()
    st.write("The portfolio's performance metrics are")
    st.write("The portfolio's expected return is ",round(portfolio_perf[0]*100,2),"%")
    st.write("The Annual Volatility is ",round(portfolio_perf[1]*100,2),"%")
    st.write("Sharpe Ratio is ",round(portfolio_perf[2],2))

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
    