# -*- coding: utf-8 -*-
"""
Created on Fri Jan 08 15:51:13 2022
@author: Joze
"""

# Raw Package
import pandas as pd
import plotly.express as px
import streamlit as st
#data
eee=pd.read_csv(r'https://github.com/JozeHladnik/streamlit-example/blob/master/slovenia2karstsecforest_DB_1000_roistats.csv?raw=true', header=17)
col= eee.columns
#col= ['date', 'local_std_time', 'doy', 'filename', 'solar_elev', 'exposure',
#        'awbflag', 'mask_index', 'gcc', 'rcc', 'r_mean', 'r_std', 'r_5_qtl',
#        'r_10_qtl', 'r_25_qtl', 'r_50_qtl', 'r_75_qtl', 'r_90_qtl', 'r_95_qtl',
#        'g_mean', 'g_std', 'g_5_qtl', 'g_10_qtl', 'g_25_qtl', 'g_50_qtl',
#        'g_75_qtl', 'g_90_qtl', 'g_95_qtl', 'b_mean', 'b_std', 'b_5_qtl',
#        'b_10_qtl', 'b_25_qtl', 'b_50_qtl', 'b_75_qtl', 'b_90_qtl', 'b_95_qtl',
#        'r_g_correl', 'g_b_correl', 'b_r_correl'],
#       dtype='object'
"""
##Pregled podatkov v tabeli: 
slovenia2karstsecforest_DB_1000_roistats.csv 
##pridobljen iz:
https://phenocam.sr.unh.edu/webcam/roi/slovenia2karstsecforest/DB_1000/
## Jožetov projekt 
Meni je Streamlit zelo :heart:všeč:heart:.
"""
#symbol = st.sidebar.radio("Izberi kateri simbol naj prikaže v desni",col)
st.sidebar.write('#Idoloči graf ')
xx = st.sidebar.selectbox('Izberi os X',col,1 )
yy = st.sidebar.selectbox('Izberi os Y',col,4)
bb = st.sidebar.selectbox('Izberi simbol barve',col,2)
vv = st.sidebar.selectbox('Izberi simbol velikosti',col,5)

st.sidebar.write('X bo: ', xx)
st.sidebar.write('Y bo: ', yy)
st.sidebar.write('Barva krogcev: ',bb)
st.sidebar.write('Velikost krogcev: ',vv)
                 
                 
ee=eee.sort_values(xx,ignore_index=True)
pd.to_numeric(eee[bb], downcast='float')
pd.to_numeric(eee[vv], downcast='float')
pd.to_numeric(eee[yy], downcast='float')

fig = px.scatter(ee, x=xx, y=yy, color=bb, #'exposure',
                 size=vv, hover_data=['filename'])


#fig.show()
st.plotly_chart(fig)



st.write(' - - - podatki v tabeli - - ')
st.write(ee)
