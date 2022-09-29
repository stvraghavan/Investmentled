import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sb
from datetime import date
from nsepy import get_history as gh
plt.style.use('fivethirtyeight') #setting matplotlib style

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import  risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

st.title("Stockfolio💲💲💲")

tab1,tab2 = st.tabs(["Stock Tracker","Portfolio Optimiser"])

with tab1:
    
    with st.expander("Stock Symbols"):
        NSE_data = pd.read_csv("F:\jupyter\Stockfolio-main\EQUITY_L.csv")
        NSE_data = NSE_data[NSE_data['SERIES'] == 'EQ']
        st.write(NSE_data[['NAME OF COMPANY','SYMBOL']])
        
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

    fig, ax = plt.subplots(figsize=(15,8))
    for i in df.columns.values :
        ax.plot(df[i], label = i)
    ax.set_title("Portfolio Close Price History")
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('Close Price INR (Rs)' , fontsize=18)
    ax.legend(df.columns.values , loc = 'upper left')
    st.pyplot(fig)
    ## st.write("The plot shows the History of closing price(INR) of stocks") 

    correlation_matrix = df.corr(method='pearson')
    #correlation_matrix

    fig1 = plt.figure()
    sb.heatmap(correlation_matrix,xticklabels=correlation_matrix.columns, yticklabels=correlation_matrix.columns,
    cmap='YlGnBu', annot=True, linewidth=0.5)
    st.write('Correlation between Stocks in your portfolio')
    st.pyplot(fig1)

    daily_simple_return = df.pct_change(1)
    daily_simple_return.dropna(inplace=True)
    #daily_simple_return

    st.write('Daily simple returns')
    fig, ax = plt.subplots(figsize=(15,8))


    for i in daily_simple_return.columns.values :
        ax.plot(daily_simple_return[i], lw =2 ,label = i)


    ax.legend( loc = 'upper right' , fontsize =10)
    ax.set_title('Volatility in Daily simple returns ')
    ax.set_xlabel('Date')
    ax.set_ylabel('Daily simple returns')
    st.pyplot(fig)
    ## st.write("The figure depicts the volatility in Daily Simple returns of stocks produced at end of the day")
    ## with st.expander("Volatility")
    ## st.write("liability to change rapidly and unpredictably, especially for the worse.")
    ## st.write("If the price of a stock fluctuates rapidly in a short period, hitting new highs and lows, it is said to have high volatility.") 
    ## st.write("If the stock price moves higher or lower more slowly, or stays relatively stable, it is said to have low volatility.")

    st.write('Average Daily returns(%) of stocks in your portfolio')
    Avg_daily = daily_simple_return.mean()
    st.write(Avg_daily*100)

    daily_simple_return.plot(kind = "box",figsize = (20,10), title = "Risk Box Plot")

    st.write('Annualized Standard Deviation (Volatality(%), 252 trading days) of individual stocks in your portfolio on the basis of daily simple returns.')
    st.write(daily_simple_return.std() * np.sqrt(252) * 100)

    Avg_daily / (daily_simple_return.std() * np.sqrt(252)) *100

    daily_cummulative_simple_return =(daily_simple_return+1).cumprod()
    #daily_cummulative_simple_return

    #visualize the daily cummulative simple return
    st.write('Cummulative Returns')
    fig, ax = plt.subplots(figsize=(18,8))
    ## st.write("This plot visualize the stocks based on their daily cummulative simple returns")
    

    for i in daily_cummulative_simple_return.columns.values :
        ax.plot(daily_cummulative_simple_return[i], lw =2 ,label = i)

    ax.legend( loc = 'upper left' , fontsize =10)
    ax.set_title('Daily Cummulative Simple returns/growth of investment')
    ax.set_xlabel('Date')
    ax.set_ylabel('Growth of ₨ 1 investment')
    st.pyplot(fig)
    ## st.write(The above plot depicts the ratio/variation between the Date & Growth of Rs1 investment")
    
with tab2:

    mean = expected_returns.mean_historical_return(df)

    S = risk_models.sample_cov(df) # for sample covariance matrix
    #S

    plt.style.use('ggplot')
    fig = plt.figure()
    sb.heatmap(S,xticklabels=S.columns, yticklabels=S.columns,
    cmap='RdBu_r', annot=True, linewidth=0.5)
    st.write('Covariance between daily simple returns of stocks in your portfolio')
    st.pyplot(fig)

    ef = EfficientFrontier(mean,S)
    weights = ef.max_sharpe() #for maximizing the Sharpe ratio #Optimization
    cleaned_weights = ef.clean_weights() #to clean the raw weights
    # Get the Keys and store them in a list
    labels = list(cleaned_weights.keys())
    # Get the Values and store them in a list
    values = list(cleaned_weights.values())
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.0f%%')
    st.write('Portfolio Allocation')
    st.pyplot(fig)

    #st.write(ef.portfolio_performance(verbose=True))
    portfolio_perf = ef.portfolio_performance()
    st.write("The portfolio's performance metrics are")
    st.write("The portfolio's expected return is ",round(portfolio_perf[0]*100,2),"%")
    st.write("The Annual Volatility is ",round(portfolio_perf[1]*100,2),"%")
    st.write("Sharpe Ratio is ",round(portfolio_perf[2],2))

    portfolio_amount = float(st.text_input("Enter the amount you want to invest: "))
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
    