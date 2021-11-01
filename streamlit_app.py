# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 20:28:10 2021

@author: Joze
"""
from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

"""
# Welcome to Streamlit!
## To je Jožetova predelava applikacije
Podatki so v `/streamlit_app.py` ki ga lahko predelujem kakor mi :heart: poželi!
Če imaš vprašanja si preberi [documentacijo](https://docs.streamlit.io) in [community
forums](https://discuss.streamlit.io).
Spodaj pa je prikaz code:
"""


#with st.echo(code_location='below'): #to dodaja kodo spodaj (v inted) na displej
total_points = st.slider("Število točk", 1, 500, 200)
num_turns = st.slider("Število obratov", 1, 100, 9)

Point = namedtuple('Point', 'x y')
data = []

points_per_turn = total_points / num_turns

for curr_point_num in range(total_points):
    curr_turn, i = divmod(curr_point_num, points_per_turn)
    angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
    radius = curr_point_num / total_points
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    data.append(Point(x, y))
st.write('izbrani parametri: število obratov-', num_turns,' število točk/obrat',total_points)
st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
    .mark_circle(color='#0060c9', opacity=0.4)
    .encode(x='x:Q', y='y:Q'))
