
## importing all the necessary libraries

import yfinance as yf
from datetime import date

import pandas as pd
import numpy as np
import streamlit as st

import plotly.express as px
import plotly.graph_objs as go

from config import sign_up, fetch_users

import pickle

## TITLE OF THE WEBSITE
st.title("STOCKET APP")

## making user-interactive for the user to choose its equity options
ticker = st.sidebar.text_input('SYMBOL')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')


## extracting the live data from the YAHOO finance website
Stock_symbol = ticker

stock_data = yf.download(Stock_symbol, start = start_date, end = end_date)  
stock_data

visualizations,  technical_analysis, model, news, education = st.tabs(["Portfolio Analysis","Technical Analysis Dashboard", "ML MODEL", "Financial News", "Learn Technalities"])

## making detailed analysis of the given portfolio
with visualizations:
    # Making visulaizations for the proper analysis of the given market portfolio

    ## creating the line plot for the open price of the given symbol
    fig = px.line(stock_data, x = stock_data.index , y = stock_data['Open'], title='Open price of the given stock')
    st.plotly_chart(fig)

    ## creating the line plot for the closing price of the given symbol
    fig = px.line(stock_data, x = stock_data.index , y = stock_data['Close'], title='Closing price of the given stock')
    st.plotly_chart(fig)

    ## creating the line plot for the closing price of the given symbol
    fig = px.line(stock_data, x = stock_data.index , y = stock_data['High'], title='Highest price of the given stock')
    st.plotly_chart(fig)


    ## investigating on the moving avergae of our market portfolios
    window = 50
    ts = stock_data['Close']
        
    ## making the moving average
    ts_moving_avg = ts.rolling(window = window).mean()

    ## making the plots on the moving average of our given stocks
    stock_data['Price'] = stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
    fig = px.line(stock_data, x = stock_data.index, y = stock_data['Price'], title='50-day SMA', labels={"50-dat SMA"})
    fig.update_traces(line = dict(color='green'))
    st.plotly_chart(fig)

    ## calculating the 200 day moving average of the given ticker
    stock_data['Price'] = stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()
    fig = px.line(stock_data, x = stock_data.index, y = stock_data['Price'], title='200-day SMA', labels={"200-dat SMA"})
    st.plotly_chart(fig)

    # plotting the EXPONENTIAL MOVING AVERAGE GRAPH(EMA)

    ## the adjust is kept as 'false' in order to calculate the fixed number of periods regardless of any missing values

    stock_data['Price'] = stock_data['EMA_50'] = stock_data['Close'].ewm(span=50, adjust = False).mean()
    fig = px.line(stock_data, x = stock_data.index, y = stock_data['Price'], title='50-day EMA', labels={"50-dat EMA"})
    fig.update_traces(line = dict(color='red'))
    st.plotly_chart(fig)

    ## plotting the PCR of the opening prices of stock chart

    stock_data['Price'] = stock_data['PCR'] = stock_data['Open'].pct_change(periods=50)*100
    fig = px.line(stock_data, x = stock_data.index, y = stock_data['Price'], title='PCR of 50days', labels={"50-dat EMA"})
    fig.update_traces(line = dict(color='red'))
    st.plotly_chart(fig)

    ## creating the candle stivk plot for the given stock symbol
    st.subheader('CandleStick chart for the given equity portfolio')
    fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                open = stock_data['Open'],
                high = stock_data['High'],
                low = stock_data['Low'],
                close = stock_data['Close'])])
    st.plotly_chart(fig)

## making the technical analysis dashboard for the user with having more than 100 indicators features
import pandas_ta as ta
with technical_analysis:
    st.subheader("Technical Analysis Dashboard")

    stock_data = pd.DataFrame()
    stock_data = yf.download(Stock_symbol, start = start_date, end = end_date)
    ind_list = stock_data.ta.indicators(as_list = True)
    ##st.write(ind_list)

    technical_indicator = st.selectbox("Technical Indicator", options = ind_list)
    method = technical_indicator
    indicator=pd.DataFrame(getattr(ta, method)(low=stock_data['Low'], high=stock_data['High'], close=stock_data['Close'], open=stock_data['Open'], volume=stock_data['Volume']))
    indicator['Close'] = stock_data['Close']
    figW_ind_new = px.line(indicator)
    st.plotly_chart(figW_ind_new)
    st.write(indicator)


# creation of the education tab

with education:
    st.header(f'Financial Knowledge')
    st.write('What is Opening Price:')
    st.write("The opening price is the price of a stock at the beginning of a trading session. It is the first price at which a stock is traded when the market opens for the day.")

    st.write('What is Closing Price:')
    st.write("The closing price is the final price at which a stock is traded during a trading session. It represents the last transaction price before the market closes for the day.")

    st.write('What is High Price:')
    st.write("The high price is the highest price at which a stock was traded during a given trading session.")

    st.write('What is Low Price:')
    st.write("The low price is the lowest price at which a stock was traded during a given trading session.")

    st.write('What is Moving Average:')
    st.write("Moving Average (MA) is a widely used indicator in technical analysis that helps smooth out price data by creating a constantly updated average price. It can help identify trends and reversals.")

    st.write('What is Exponential Moving Average:')
    st.write("Exponential Moving Average (EMA) is a type of moving average that gives more weight to recent prices. It reacts more quickly to price changes compared to a simple moving average.")

    st.write('What is Percentage Change (PCR):')
    st.write("Percentage Change (PCR) is a measure of the price change expressed as a percentage. It is often used to measure the price movement of stocks or other financial instruments.")

    st.write('What is Candlestick Chart:')
    st.write("A candlestick chart is a graphical representation of price movement in financial markets. Each candlestick typically represents a single trading day and shows the opening, closing, high, and low prices.")

    st.write('What is LSTM (Long Short-Term Memory):')
    st.write("LSTM is a type of recurrent neural network (RNN) architecture used in the field of deep learning. It is particularly useful for time series data and sequential tasks due to its ability to capture long-term dependencies.")

    st.write('What is Sentiment Analysis:')
    st.write("Sentiment analysis involves using natural language processing and machine learning techniques to determine the sentiment or emotional tone of a piece of text. In the context of financial news, it can help gauge market sentiment.")

    st.write('Feel free to explore more about these concepts and improve your understanding of the financial markets!')

## implementing the LSTM model for the given equity
import tensorflow as tf
import math
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score 

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM


with model:

    stock_data = yf.download(Stock_symbol, start = start_date, end = end_date)
    stock_data.reset_index(inplace = True)

    ## taking the closing price for the training of the model
    df = stock_data.reset_index()['Close']

    scaler=MinMaxScaler(feature_range=(0,1))
    df=scaler.fit_transform(np.array(df).reshape(-1,1))

    ## splitting of the dataset
    training_size=int(len(df)*0.65)
    test_size=len(df)-training_size
    train_data,test_data=df[0:training_size,:],df[training_size:len(df),:1]

    def create_dataset(dataset, time_step=1):
        dataX, dataY = [], []
        for i in range(len(dataset)-time_step-1):
            a = dataset[i:(i+time_step), 0]   ###i=0, 0,1,2,3-----99   100 
            dataX.append(a)
            dataY.append(dataset[i + time_step, 0])
        return np.array(dataX), np.array(dataY)


    time_step = 100
    X_train, y_train = create_dataset(train_data, time_step)
    X_test, ytest = create_dataset(test_data, time_step)

    # reshape input to be [samples, time steps, features] which is required for LSTM
    X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)


    model=Sequential()
    model.add(LSTM(50,return_sequences=True,input_shape=(100,1)))
    model.add(LSTM(50,return_sequences=True))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error',optimizer='adam')

    model.fit(X_train,y_train,validation_data=(X_test,ytest),epochs=30,batch_size=64,verbose=1)

    st.title("LSTM Model in Streamlit")

    st.write("This app demonstrates how to implement an LSTM model in Streamlit.")

    if st.button("Predict"):
        prediction = model.predict(X_train[-1].reshape(1, X_train.shape[1], X_train.shape[2]))
        prediction = scaler.inverse_transform(prediction)
        st.write("Prediction:", prediction)


## Showing the financial news
from stocknews import StockNews
import streamlit as st

with st.expander("Finance News"):
    st.header('News of FINANCE')
    sn = StockNews(ticker, save_news=False)
    df_news = sn.read_rss()

    # Ensure that there are at least 10 news items in the DataFrame
    num_news_items = min(10, len(df_news))

    for i in range(num_news_items):
        st.subheader(f'News {i+1}')
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment {title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]  # Corrected column name
        st.write(f'News Sentiment {news_sentiment}')




