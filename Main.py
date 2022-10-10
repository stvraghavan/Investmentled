#Importing streamlit

import streamlit as st

st.title("Welcom to Stockfolio!! 💲💲💲")

st.header('Stockfolio is your destination to finding insights about stocks.')

st.markdown("""
    
        We provide a variety of services ranging from
    
        1. Stock tracking📈
        2. Sentiment analysis of news and twitter😀😍😫😔☹️😨🤯😭
        3. Portfolio optimiser🎯🐂🐻

        **We use Open-Source software to provide you with the service so it's perfectly safe and free**

 """)

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
with col2:
        with st.expander("Why Sentiment Analysis?"):
                st.write("""
                The stock market is a highly volatile entity affect by many people and people themselves are affect by social factors.
                By Performing sentiment analysis we can capture some of the sentiments they express online to gain a small insight on how they might influence the market. 
                """)
        # with st.expander("How do we give you future stock prices"):
        #         st.write("""
        #         We used a statistical model called Auto-Regressive Integrated Moving Average Model or ARIMA Model to estimate the future stock prices. 
        #         The model was tested to provide maximum accuracy possible.
        #         """)


st.caption("Remember the analysis work done here is only for gaining information, we are in no way responsible for any money you gain / lose. Investment in stocks is subject to market risks please make sure to read all documents carefully")
