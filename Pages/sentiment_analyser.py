import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
from wordcloud import WordCloud, STOPWORDS
import numpy as np
import re
import snscrape.modules.twitter as sntwitter
import plotly.express as px

nltk.download('vader_lexicon') #required for Sentiment Analysis

tab1,tab2 = st.tabs(["Google News","Twitter"])

with tab1:
    now = dt.date.today()
    now = now.strftime('%m-%d-%Y')
    yesterday = dt.date.today() - dt.timedelta(days = 1)
    yesterday = yesterday.strftime('%m-%d-%Y')

    nltk.download('punkt')
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 10

    # save the company name in a variable
    company_name = st.text_input("Please provide the name of the Company or a Ticker: ")
    #As long as the company name is valid, not empty...
    if company_name != '':
        st.write(f'Searching for and analyzing {company_name}, Please be patient, it might take a while...')

        #Extract News with Google News
        googlenews = GoogleNews(start=yesterday,end=now)
        googlenews.search(company_name)
        result = googlenews.result()
        #store the results
        df = pd.DataFrame(result)
        st.write(df)

    try:
        list =[] #creating an empty list 
        for i in df.index:
            dict = {} #creating an empty dictionary to append an article in every single iteration
            article = Article(df['link'][i],config=config) #providing the link
            try:
                article.download() #downloading the article 
                article.parse() #parsing the article
                article.nlp() #performing natural language processing (nlp)
            except:
                pass 
            #storing results in our empty dictionary
            dict['Date']=df['date'][i] 
            dict['Media']=df['media'][i]
            dict['Title']=article.title
            dict['Article']=article.text
            dict['Summary']=article.summary
            dict['Key_words']=article.keywords
            list.append(dict)
        check_empty = not any(list)
        # print(check_empty)
        if check_empty == False:
            news_df=pd.DataFrame(list) #creating dataframe
            st.write(news_df)

    except Exception as e:
        #exception handling
        st.write("exception occurred:" + str(e))
        st.write('Looks like, there is some error in retrieving the data, Please try again or try with a different ticker.' )

    #Sentiment Analysis
    def percentage(part,whole):
        return 100 * float(part)/float(whole)

    #Assigning Initial Values
    positive = 0
    negative = 0
    neutral = 0
    #Creating empty lists
    news_list = []
    neutral_list = []
    negative_list = []
    positive_list = []

    #Iterating over the tweets in the dataframe
    for news in news_df['Summary']:
        news_list.append(news)
        analyzer = SentimentIntensityAnalyzer().polarity_scores(news)
        neg = analyzer['neg']
        neu = analyzer['neu']
        pos = analyzer['pos']
        comp = analyzer['compound']

        if neg > pos:
            negative_list.append(news) #appending the news that satisfies this condition
            negative += 1 #increasing the count by 1
        elif pos > neg:
            positive_list.append(news) #appending the news that satisfies this condition
            positive += 1 #increasing the count by 1
        elif pos == neg:
            neutral_list.append(news) #appending the news that satisfies this condition
            neutral += 1 #increasing the count by 1 

    positive = percentage(positive, len(news_df)) #percentage is the function defined above
    negative = percentage(negative, len(news_df))
    neutral = percentage(neutral, len(news_df))

    #Converting lists to pandas dataframe
    news_list = pd.DataFrame(news_list)
    neutral_list = pd.DataFrame(neutral_list)
    negative_list = pd.DataFrame(negative_list)
    positive_list = pd.DataFrame(positive_list)
    #using len(length) function for counting
    st.write("Positive Sentiment:", '%.2f' % len(positive_list), end='\n')
    st.write("Neutral Sentiment:", '%.2f' % len(neutral_list), end='\n')
    st.write("Negative Sentiment:", '%.2f' % len(negative_list), end='\n')

    #Creating PieCart
    labels = ['Positive ['+str(round(positive))+'%]' , 'Neutral ['+str(round(neutral))+'%]','Negative ['+str(round(negative))+'%]']
    sizes = [positive, neutral, negative]
    colors = ['yellowgreen', 'blue','red']
    fig = px.pie(sizes,values=sizes,names=labels,color=labels,
                color_discrete_map={
                    'Positive ['+str(round(positive))+'%]':'green',
                    'Neutral ['+str(round(neutral))+'%]':'blue',
                    'Negative ['+str(round(negative))+'%]':'red'
                },title="Sentiment Analyser for company"+company_name+"")
    st.plotly_chart(fig)

    # Word cloud visualization
    def word_cloud(text):
        stopwords = set(STOPWORDS)
        allWords = ' '.join([nws for nws in text])
        wordCloud = WordCloud(background_color='black',width = 1600, height = 800,stopwords = stopwords,min_font_size = 20,max_font_size=150,colormap='prism').generate(allWords)
        fig, ax = plt.subplots(figsize=(20,10), facecolor='k')
        plt.imshow(wordCloud)
        ax.axis("off")
        fig.tight_layout(pad=0)
        st.pyplot(fig)

    st.write('Wordcloud for ' + company_name)
    word_cloud(news_df['Summary'].values)

with tab2:
    #Get user input
    query = company_name

    #As long as the query is valid (not empty or equal to '#')...
    if query != '':
        noOfTweet = '100'
        if noOfTweet != '' :
            noOfDays = '2'
            if noOfDays != '':
                    #Creating list to append tweet data
                    tweets_list = []
                    now = dt.date.today()
                    now = now.strftime('%Y-%m-%d')
                    yesterday = dt.date.today() - dt.timedelta(days = int(noOfDays))
                    yesterday = yesterday.strftime('%Y-%m-%d')
                    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query + ' lang:en since:' +  yesterday + ' until:' + now + ' -filter:links -filter:replies').get_items()):
                        if i > int(noOfTweet):
                            break
                        tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.username])

                    #Creating a dataframe from the tweets list above 
                    df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

                    st.write(df)

    # Create a function to clean the tweets
    def cleanTxt(text):
        text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
        text = re.sub('#', '', text) # Removing '#' hash tag
        text = re.sub('RT[\s]+', '', text) # Removing RT
        text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
        return text

    #applying this function to Text column of our dataframe
    df["Text"] = df["Text"].apply(cleanTxt)

    #Sentiment Analysis
    def percentage(part,whole):
        return 100 * float(part)/float(whole)

    #Assigning Initial Values
    positive = 0
    negative = 0
    neutral = 0
    #Creating empty lists
    tweet_list1 = []
    neutral_list = []
    negative_list = []
    positive_list = []

    #Iterating over the tweets in the dataframe
    for tweet in df['Text']:
        tweet_list1.append(tweet)
        analyzer = SentimentIntensityAnalyzer().polarity_scores(tweet)
        neg = analyzer['neg']
        neu = analyzer['neu']
        pos = analyzer['pos']
        comp = analyzer['compound']

        if neg > pos:
            negative_list.append(tweet) #appending the tweet that satisfies this condition
            negative += 1 #increasing the count by 1
        elif pos > neg:
            positive_list.append(tweet) #appending the tweet that satisfies this condition
            positive += 1 #increasing the count by 1
        elif pos == neg:
            neutral_list.append(tweet) #appending the tweet that satisfies this condition
            neutral += 1 #increasing the count by 1 

    positive = percentage(positive, len(df)) #percentage is the function defined above
    negative = percentage(negative, len(df))
    neutral = percentage(neutral, len(df))

    #Converting lists to pandas dataframe
    tweet_list1 = pd.DataFrame(tweet_list1)
    neutral_list = pd.DataFrame(neutral_list)
    negative_list = pd.DataFrame(negative_list)
    positive_list = pd.DataFrame(positive_list)
    #using len(length) function for counting
    st.write("Since " + noOfDays + " days, there have been", len(tweet_list1) ,  "tweets on " + query, end='\n*')
    st.write("Positive Sentiment:", '%.2f' % len(positive_list), end='\n*')
    st.write("Neutral Sentiment:", '%.2f' % len(neutral_list), end='\n*')
    st.write("Negative Sentiment:", '%.2f' % len(negative_list), end='\n*')

    #Creating PieCart**

    labels = ['Positive ['+str(round(positive))+'%]' , 'Neutral ['+str(round(neutral))+'%]','Negative ['+str(round(negative))+'%]']
    sizes = [positive, neutral, negative]
    colors = ['yellowgreen', 'blue','red']
    fig = px.pie(sizes,values=sizes,names=labels,color=labels,
                color_discrete_map={
                    'Positive ['+str(round(positive))+'%]':'green',
                    'Neutral ['+str(round(neutral))+'%]':'blue',
                    'Negative ['+str(round(negative))+'%]':'red'
                },title="Sentiment Analysis Result for keyword= "+query+"")
    st.plotly_chart(fig)
    

    # word cloud visualization
    def word_cloud(text):
        stopwords = set(STOPWORDS)
        allWords = ' '.join([twts for twts in text])
        wordCloud = WordCloud(background_color='black',width = 1600, height = 800,stopwords = stopwords,min_font_size = 20,max_font_size=150,colormap='prism').generate(allWords)
        fig, ax = plt.subplots(figsize=(20,10), facecolor='k')
        plt.imshow(wordCloud)
        ax.axis("off")
        fig.tight_layout(pad=0)
        st.pyplot(fig)

    st.write('Wordcloud for ' + query)
    word_cloud(df['Text'].values)