import pandas as pd
import numpy as np
from nsepy import get_history as gh
from tqdm import tqdm
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Developer's Courtesy",page_icon="🛠")

def get_50data():
    symbols = pd.read_csv("Data/ind_nifty50list.csv")
    return symbols

def get_all_data():
    symbols = pd.read_csv("Data/EQUITY_L.csv")
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

code_make_data = '''def make_data(stocksymbols,startdate,end_date):
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
    return data_frame'''
code_daily_simple_return ='''def daily_simple_return(data_frame):
    dsr = data_frame.pct_change(1)
    dsr.dropna(inplace=True)
    return dsr'''
code_daily_simple_return_percent = '''def daily_simple_return_percent(data_frame):
    Avg_daily = data_frame.mean().rename('Average Return')
    Avg_daily = Avg_daily*100
    return Avg_daily'''

code_word_cloud ='''
def word_cloud(text):
        stopwords = set(STOPWORDS)
        allWords = ' '.join([nws for nws in text])
        wordCloud = WordCloud(background_color='black',width = 1600, height = 800,stopwords = stopwords,min_font_size = 20,max_font_size=150,colormap='prism').generate(allWords)
        fig, ax = plt.subplots(figsize=(20,10), facecolor='k')
        plt.imshow(wordCloud)
        ax.axis("off")
        fig.tight_layout(pad=0)
        st.pyplot(fig)
'''
code_libraries ='''
pandas
numpy
nsepy
wordcloud 
streamlit
pyportfolioopt
plotly
datetime
GoogleNews
nltk
snscrape
'''

st.write("Greetings to users, this pages of the application aims to share the key components of code used in the development of this application.")

st.write("Below are the list of key libraries used in this project.")
st.code(code_libraries,language="python")
st.write('''
Below is the code that was used to create a consolidated form of stock prices for processing them.
''')
st.code(code_make_data,language="python")
st.write("The below two snippets of code were used to generate the gain seen in the stock(s)")
st.code(code_daily_simple_return,language="python")
st.code(code_daily_simple_return_percent,language="python")
st.write("The below snippet of code was used to generate a word cloud for sentiment analysis")
st.code(code_word_cloud,language="python")