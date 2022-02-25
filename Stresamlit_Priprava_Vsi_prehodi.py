"""
Created on Fri Jan 08 15:51:13 2022
@author: Joze
"""
# -*- coding: utf-8 -*-
# Raw Package
import pandas as pd
import requests, json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import plotly.express as px

#DATA
TNP = [91, 92, 184, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 267, 268, 269, 270] #'zavrženi' so izpuščeni
KP_TR = [73, 98, 99, 140, 141, 142, 143, 144, 145, 146]
Kranj = [137, 138]
Golovec = [149, 150, 151, 152, 153, 154, 155, 156]
BP = [181, 182, 183]
LokPreh={'TNP':TNP,'KP_TR':KP_TR, 'Kranj':Kranj, 'Golovec':Golovec, 'BP':BP }
URLo='http://193.2.23.31/export/ecb8cb01dcc21204a926ff8d4821c217dabd131b/data?'
locations=pd.read_excel(r'https://github.com/JozeHladnik/streamlit-example/blob/master/eEMIS-DB-location-places.xlsx?raw=true',sheet_name='Locations' )
places= pd.read_excel(r'https://github.com/JozeHladnik/streamlit-example/blob/master/eEMIS-DB-location-places.xlsx?raw=true' )
place_inst=pd.read_excel(r'https://github.com/JozeHladnik/streamlit-example/blob/master/eEMIS-DB-location-places.xlsx?raw=true',sheet_name='Place_inst' )
place_instr_para=pd.read_excel(r'https://github.com/JozeHladnik/streamlit-example/blob/master/eEMIS-DB-location-places.xlsx?raw=true',sheet_name='places_instr_para' )
print(locations.columns)

#ustvariom potrebne SLOVARJE
Dloc=pd.Series(locations['name '].values,index=locations['id ']).to_dict()
Dpla=pd.Series(places['name'].values,index=places['id']).to_dict()
    
Dsmer={}
for i in range(len(place_inst['id'])): 
    df2=place_instr_para.loc[(place_instr_para['place_inst_id']==place_inst.iloc[i][0])] 
    ll=[str(df2['short_name'][2:3])[8:len(df2['short_name'][2:3])-33],str(df2['short_name'][3:4])[8:len(df2['short_name'][3:4])-33],place_inst.iloc[i][0]]
    Dsmer[place_inst.iloc[i][1]]= ll 
#določimo čas:
now=pd.Timestamp.now() 
Pmesec=str(now-pd.DateOffset(months=1))[5:7] #št. prejšnjega meseca
PmDol=pd.Period(str(now-pd.DateOffset(months=1))[:10]).days_in_month #število dni v preteklem mesecu
print(Pmesec,PmDol)
#result = sr.dt.month_name(locale = 'English')
# sr=now-pd.DateOffset(months=1)
yr= (now-pd.DateOffset(months=1)).year
# imeM=sr.month_name(locale = 'Slovenian') #dobimo ime meseca!
# print(imeM, yr)
# mesc=now-np.timedelta64(30,'D')
prviM= '2021-'+str(Pmesec)+'-01T00:01' 
zadnjiM = '2022-'+str(Pmesec)+'-'+str(PmDol)+'T23:55'

#       dtype='object'
"""
Prikaz grafikonov za izbrano Lokacijo / Merilno Mesto / Mesece
"""
#symbol = st.sidebar.radio("Izberi kateri simbol naj prikaže v desni",col)
st.sidebar.write('#Idoloči graf ')
Lok = st.sidebar.selectbox('Izberi Lokacijo',LokPreh,1 )# soustni meni 1
MM=LokPreh[Lok]
Position=st.sidebar.selectbox('Izberi Merilno mesto',MM,1) #spustni meni 2

pl= places.loc[(places['id'] == Position)]

st.sidebar.write('Nahajamo se na lokaciji: ', Lok)
st.sidebar.write('Gledamo merilno mesto: ', Position, str(pl['name'].to_string(index=False)))


URL=URLo+'place_id='+str(Position)+'&interval_code='+'D'+'&start_time='+prviM+'&end_time='+zadnjiM
print(URL)
url = requests.get(URL, timeout=20).text
data = json.loads(url)#.text)
df = pd.DataFrame(data['data'])

if len(df['data COUNT 0 E'])==0:
    st.write('ni podatkov za: ',str(pl['name']))
else:    
    df['tja']=pd.to_numeric(df['data COUNT 0 E'])
    df['nazaj']=pd.to_numeric(df['data COUNT 1 E'])
    df['cas']=pd.to_datetime(df['time_string']) #naredimo berlivo kot čas.
    df['Ocas']=df['time_string'] #nardedimo string časa za X os
    for ii in range(len(df['Ocas'])):
        df['Ocas'][ii]=df['time_string'][ii][8:10]
    df['Lmesec']=df['time_string'][:7] #nardedimo string časa za X os
    for iii in range(len(df['Ocas'])):
        df['Lmesec'][iii]=df['time_string'][iii][:7]
    lm=df['Lmesec'].unique()
    mesci = st.sidebar.multiselect('Izberi mesece',   lm)
#     st.write('izbrani meseci:', options)
#     st.write('podatki: ',df['Lmesec'])

#     LM = st.selectbox('Izberi Mesec',lm,1 )
#     df1=df.loc[(df['Lmesec']==LM)]
    for i in mesci:
        df1=df.loc[(df['Lmesec']==i)]
        width = 0.35  # the width of the bars
        polD=np.timedelta64(4,'h') #naredimo da lahko zamaknemo stolpce v grafikonu
        st.write('Mesec: ',i)
        
        fig, ax = plt.subplots(figsize=(10,2.5))  #velikost grafikona
        rects1 = ax.bar(df1['cas']-polD, df1['tja'], width, label=Dsmer[Position][0])  #dodaj oznake!!
        rects2 = ax.bar(df1['cas']+polD, df1['nazaj'], width, label=Dsmer[Position][1])
        ax.set_ylabel('Št. prehodov')
        ax.set_title('prehodi mimo senzorja '+str(pl['name'].to_string(index=False))+'_'+i)
        ax.set_xticks(df1['cas'])
        ax.set_xticklabels(df1['Ocas'])
        ax.legend()
        fig.tight_layout()
        plt.show()
        st.pyplot(fig)
    #     st.write('podatki: ',df.columns)
        # st.sidebar.write('Velikost krogcev: ',vv)


        # ee=eee.sort_values(xx,ignore_index=True)
        # pd.to_numeric(eee[bb], downcast='float')
        # pd.to_numeric(eee[vv], downcast='float')
        # pd.to_numeric(eee[yy], downcast='float')

#         fig = px.bar(df1, x='cas', y='tja')#, color='data DIAG 0 A'), #'exposure',
#         #                  size='gps_coor_y', hover_data=['modified', 'mod_user_id'])

#         st.plotly_chart(fig)
    


st.write('  Podatki za celotno leto v tabeli - - - - - ')
st.write(df)
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')

csv = convert_df(df)

st.download_button(
     label="Prenesi podatke kot CSV",
     data=csv,
     file_name='podatki_za-MerilnoMesto.csv',
     mime='text/csv' )
