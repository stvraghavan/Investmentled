import pandas as pd
import numpy as np
from nsepy import get_history as gh
from tqdm import tqdm
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import streamlit as st

def get_50data():
    symbols = pd.read_csv("Pages/Data/ind_nifty50list.csv")
    return symbols

def get_all_data():
    symbols = pd.read_csv("Pages/Data/EQUITY_L.csv")
    return symbols

def make_data(stocksymbols,startdate,end_date):
    data_frame = pd.DataFrame()
    for i in tqdm(range(len(stocksymbols))):
        try:
            data = gh(symbol=stocksymbols[i],start=startdate, end=(end_date))[['Symbol','Close']]
            data.rename(columns={'Close':data['Symbol'][0]},inplace=True)
            data.drop(['Symbol'], axis=1,inplace=True)
            if i == 0:
                data_frame = data
            if i != 0:
                data_frame = data_frame.join(data)
        except:
            pass
    return data_frame

def daily_simple_return(data_frame):
    dsr = data_frame.pct_change(1)
    dsr.dropna(inplace=True)
    # Avg_daily = list(Avg_daily)
    return dsr

def daily_simple_return_percent(data_frame):
    Avg_daily = data_frame.mean().rename('Average Return')
    Avg_daily = Avg_daily*100
    return Avg_daily

def word_cloud(text):
        stopwords = set(STOPWORDS)
        allWords = ' '.join([nws for nws in text])
        wordCloud = WordCloud(background_color='black',width = 1600, height = 800,stopwords = stopwords,min_font_size = 20,max_font_size=150,colormap='prism').generate(allWords)
        fig, ax = plt.subplots(figsize=(20,10), facecolor='k')
        plt.imshow(wordCloud)
        ax.axis("off")
        fig.tight_layout(pad=0)
        st.pyplot(fig)