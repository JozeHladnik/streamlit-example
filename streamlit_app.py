# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 15:51:13 2021

@author: Joze
"""

# Raw Package
import numpy as np
import pandas as pd
import yfinance as yf#Data Source
import streamlit as st

"""
# Pregled Forex
## To je Jožetov pregled simbolov
Podatki so v `/streamlit_app.py` na mojem Github.com. Če te zanima delovanje si preberi [documentacijo](https://docs.streamlit.io) in [community
forums](https://discuss.streamlit.io). 
Meni je Streamlit zelo :heart:všeč:heart:.

"""
symbols=['EURUSD=X', 'JPY=X', 'GBPUSD=X', 'AUDUSD=X', 'NZDUSD=X', 'EURJPY=X', 'GBPJPY=X', 'EURGBP=X', 'EURCAD=X', 
         'EURSEK=X', 'EURCHF=X', 'EURHUF=X', 'EURJPY=X', 'CNY=X', 'HKD=X', 'SGD=X', 'INR=X', 'MXN=X', 'PHP=X',
         'IDR=X', 'THB=X', 'MYR=X', 'ZAR=X', 'RUB=X']
symbol = st.sidebar.radio("Izberi",symbols)
df= yf.download(tickers=symbol, period= '1mo', interval = '30m')#, iterval = '5m')
st.write(df.head())
st.write('  - - - - ')
st.write('Današnji menjalni tečaji:')
for i in symbols:
    df= yf.download(tickers=i, period= '1mo', interval = '1d')
    st.write(i,df.Close.iloc[-1])
