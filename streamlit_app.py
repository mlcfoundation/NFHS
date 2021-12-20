'''

Sample script to visualize NFHS5 data using streamlit.io

Akshay Ranjan <akshay@mlcfoundation.org.in>

'''
from numpy import modf
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os
import csv

DATA_PATH = os.path.join('.', 'data')

st.set_page_config(
     page_title="NFHS-5 District Indicators Comparison App",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://github.com/mlcfoundation/NFHS/issues',
         'Report a bug': "https://github.com/mlcfoundation/NFHS/issues",
         'About': "# NFHS-5 District Indicators Comparison App"
     }
 )

st.title('NFHS-5')
st.header('District Comparison')
st.subheader('Select state(s) followed by district(s)')

#------------------------------------------------------------------------------
col1, col2 = st.columns(2)
with col1:
    do_table = st.checkbox('Show table',
                           value=True,
                           help='Show selected indicator and data in a table')
with col2:
    do_chart = st.checkbox('Show chart',
                           value=False,
                           help='Show selected indicator and data as a chart')

#------------------------------------------------------------------------------
def build_states_list():
    states = []
    for fe in os.scandir(DATA_PATH):
        if fe.is_dir():
            states.append(fe.name)
    return states
states = build_states_list()
selected_states = st.multiselect('State(s)', 
                                 states,
                                 help='Select one or more states')

#------------------------------------------------------------------------------
def build_districts_list(states):
    data = {}
    districts = []
    for state in states:
        for fe in os.scandir(os.path.join(DATA_PATH, state)):
            if fe.is_file():
                name = fe.name.rsplit('.', 1)[0]
                data[name] = state
                districts.append(state+', '+name)
    return data, districts
states_districts, districts = build_districts_list(selected_states)
selected_districts = st.multiselect('District(s)', 
                                    districts,
                                    help='Select one or more districts')

#------------------------------------------------------------------------------
def read_data(districts):
    #global states_districts
    data = {}
    indicators = {}

    for se in districts:
        district = se.split(',')[1].strip()
        state = se.split(',')[0].strip()
        path = os.path.join(DATA_PATH, state, district+".csv")
        df = pd.read_csv(path, delimiter=",")
        data[district] = (state, df)
    return data
data = read_data(selected_districts)

#------------------------------------------------------------------------------
def build_indicator_list(data):
    id = []
    for de in data.items():
        id = de[1][1]['Indicator'].to_list()
        break
    return id
indicators = build_indicator_list(data)
indicators_selected = st.selectbox('Indicator', 
                                    indicators,
                                    help='Select an indicator')

#------------------------------------------------------------------------------
def format_data(indicators, data):
    mdf = pd.DataFrame()
    if len(data):
        for de in data.items():
            df = de[1][1].loc[de[1][1]['Indicator'].isin([indicators])][['NFHS_5']]
            #df['State'] = de[1][0]
            df['District'] = de[1][0]+', '+de[0]
            mdf = mdf.append(df)
        mdf['NFHS_5']=mdf['NFHS_5'].str.replace(',','')
        #mdf.set_index('District', drop=True, inplace=True)
        mdf['NFHS_5']=pd.to_numeric(mdf['NFHS_5'])
        mdf.columns=['NFHS_5','District']
        mdf = mdf[['District', 'NFHS_5']]
        mdf.reset_index(inplace=True, drop=True)
    return mdf
mdata = format_data(indicators_selected, data)

if do_table:
    st.table(mdata)

if do_chart:
    c = alt.Chart(mdata).mark_bar().encode(x='NFHS_5:Q', y='District:O')
    txt = c.mark_text(align='left', baseline= 'middle', dx= 3).encode(text='NFHS_5:Q')
    rule = alt.Chart(mdata).mark_rule(color='red').encode(x='mean(NFHS_5):Q')
    st.altair_chart((c+txt+rule), use_container_width=True)


        



    

