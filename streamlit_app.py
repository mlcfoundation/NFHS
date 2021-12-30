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
                if name not in ['Indicators', 'SampleInfo']:
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
def read_info(states, districts):
    mdf = pd.DataFrame()
    for state in states:
        for fe in os.scandir(os.path.join(DATA_PATH, state)):
            if fe.is_file() and fe.name == 'SampleInfo.csv':
                df = pd.read_csv(fe.path)
                mdf = mdf.append(df)
    mdf.set_index('District', inplace=True, drop=True)
    mdf = mdf.loc[[ d.split(',')[1].strip() for d in districts ], ['Households','Women','Men']]
    return mdf
info = None
if len(selected_districts) !=0:
    info = read_info(selected_states, selected_districts)

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
#'''
def format_data(indicators, data):
    mdf = pd.DataFrame()
    if len(data):
        for de in data.items():
            df = de[1][1].loc[de[1][1]['Indicator'].isin([indicators])][['NFHS-5']]
            #df['State'] = de[1][0]
            df['District'] = de[1][0]+', '+de[0]
            mdf = mdf.append(df)
        mdf['NFHS-5']=mdf['NFHS-5'].str.replace(',','')
        mdf['NFHS-5']=mdf['NFHS-5'].str.replace('(','')
        mdf['NFHS-5']=mdf['NFHS-5'].str.replace(')','')
        #mdf.set_index('District', drop=True, inplace=True)
        mdf['NFHS-5']=pd.to_numeric(mdf['NFHS-5'])
        mdf.columns=['NFHS-5','District']
        mdf = mdf[['District', 'NFHS-5']]
        mdf.reset_index(inplace=True, drop=True)
    return mdf
mdata = format_data(indicators_selected, data)

with st.expander('Sample Data', expanded=True):
    colHH, colW, colM = st.columns(3)
    if info is not None:
        colHH.metric('Households', info.sum()['Households'])
        colW.metric('Women', info.sum()['Women'])
        colM.metric('Men', info.sum()['Men'])

if do_table:
    st.dataframe(mdata)

if do_chart:
    c = alt.Chart(mdata).mark_bar().encode(x='NFHS-5:Q', y='District:O')
    txt = c.mark_text(align='left', baseline= 'middle', dx= 3).encode(text='NFHS-5:Q')
    #rule = alt.Chart(mdata).mark_rule(color='red').encode(x='mean(NFHS_5):Q')
    st.altair_chart((c+txt), use_container_width=True)


        



    

