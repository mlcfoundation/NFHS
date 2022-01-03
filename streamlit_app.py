'''

Sample script to visualize NFHS5 data using streamlit.io

Akshay Ranjan <akshay@mlcfoundation.org.in>

'''
from numpy import modf
from pandas.core.frame import DataFrame
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import os
import plotly.express as pex

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

TEXT1 = "This app is developed by *[MLC Foundation](https://www.mlcfoundation.org.in/)* using data extracted from "\
        "NFHS report PDF files available at *[NFHS](http://rchiips.org/nfhs/factsheet_NFHS-5.shtml)* "\
        "website."
TEXT2 = "Please contact Aalok Ranjan *<aalok@mlcfoundation.org.in>* or "\
        "Akshay Ranjan *<akshay@mlcfoundation.org.in>* for any help, "\
        "suggestions, questions, etc."
TEXT3 = "This is an open source application and code can be found at "\
        "*[github.com](https://github.com/mlcfoundation/NFHS)*. Report bugs "\
        "*[here](https://github.com/mlcfoundation/NFHS/issues)*."

st.sidebar.write("# **NFHS** __Data Explorer__")
st.sidebar.write("***")
st.sidebar.write('## District & State Comparison')
st.sidebar.write(TEXT1)
st.sidebar.write(TEXT2)
st.sidebar.write(TEXT3)
st.sidebar.write("***")
st.sidebar.write('Copyright (C) **MLC Foundation**. *All rights reserved.*')

#------------------------------------------------------------------------------
with st.expander('Show Options', expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        do_table = st.checkbox('Table',
                               value=True,
                               help='Show selected indicator and data in a table')
    with col2:
        do_chart = st.checkbox('Chart',
                               value=False,
                               help='Show selected indicator and data as a chart')
    with col3:
        do_nfhs4 = st.checkbox('NFHS-4',
                               value=False,
                               help='Show NFHS-4 data if available')

#------------------------------------------------------------------------------
def state_dist_to_state_dist_dict(districts_states):
    db = {}
    for district_state in districts_states:
        district = district_state.split(',')[0]
        state = district_state.split(',')[1].strip()
        if state not in db:
            db[state] = []
        db[state].append(district)
    return db

#------------------------------------------------------------------------------
def build_states_list():
    df = pd.read_csv(os.path.join(DATA_PATH, 'SampleInfo.csv'))
    return [ state.strip() for state in list(df['State']) ]
states = build_states_list()
selected_states = st.multiselect('State', 
                                 states,
                                 help='Select one or more states')

#------------------------------------------------------------------------------
def build_districts_list(states):
    districts = []
    for state in states:
        df = pd.read_csv(os.path.join(DATA_PATH, state, 'SampleInfo.csv'))
        districts = districts + ([ (district + ', ' + state) for district in list(df['District']) ])
    return districts
districts = build_districts_list(selected_states)
selected_districts = st.multiselect('District', districts, help='Select one or more districts')

#------------------------------------------------------------------------------
indicators = None
def build_state_indicators_list(states):
    indicators = []
    for state in states:
        df = pd.read_csv(os.path.join(DATA_PATH, state, 'Indicators.csv'))
        indicators = list(df['Indicator'])
        break
    return indicators

def build_district_indicators_list(districts_states):
    indicators = []
    for district_state in districts_states:
        t = district_state.split(',')
        df = pd.read_csv(os.path.join(DATA_PATH, t[1].strip(), t[0]+'.csv'))
        indicators = list(df['Indicator'])
        break
    return indicators

#------------------------------------------------------------------------------
info = None
def read_state_info(states):
    df = pd.read_csv(os.path.join(DATA_PATH, 'SampleInfo.csv'))
    return df[df['State'].isin(states)]

def read_district_info(districts_states):
    mdf = pd.DataFrame()
    db = state_dist_to_state_dist_dict(districts_states)
    for state, districts in db.items():
        df = pd.read_csv(os.path.join(DATA_PATH, state, 'SampleInfo.csv'))
        mdf = mdf.append(df[df['District'].isin(districts)])
    return mdf.reindex()

#------------------------------------------------------------------------------

data = None
def sanitize_data(mdf):
    if len(selected_districts) == 0:
        mdf['NFHS-5 Rural'] = mdf['NFHS-5 Rural'].str.replace(",","")
        mdf['NFHS-5 Urban'] = mdf['NFHS-5 Urban'].str.replace(",","")
        mdf['NFHS-5 Total'] = mdf['NFHS-5 Total'].str.replace(",","")
        mdf['NFHS-5 Rural'] = mdf['NFHS-5 Rural'].str.replace("(","")
        mdf['NFHS-5 Urban'] = mdf['NFHS-5 Urban'].str.replace("(","")
        mdf['NFHS-5 Total'] = mdf['NFHS-5 Total'].str.replace("(","")
        mdf['NFHS-5 Rural'] = mdf['NFHS-5 Rural'].str.replace(")","")
        mdf['NFHS-5 Urban'] = mdf['NFHS-5 Urban'].str.replace(")","")
        mdf['NFHS-5 Total'] = mdf['NFHS-5 Total'].str.replace(")","")        
        mdf['NFHS-5 Rural'] = pd.to_numeric(mdf['NFHS-5 Rural'])
        mdf['NFHS-5 Urban'] = pd.to_numeric(mdf['NFHS-5 Urban'])
        mdf['NFHS-5 Total'] = pd.to_numeric(mdf['NFHS-5 Total'])
        if do_nfhs4:
            mdf['NFHS-4 Total'] = mdf['NFHS-4 Total'].str.replace(",","")
            mdf['NFHS-4 Total'] = mdf['NFHS-4 Total'].str.replace("(","")
            mdf['NFHS-4 Total'] = mdf['NFHS-4 Total'].str.replace(")","")
            mdf['NFHS-4 Total'] = mdf['NFHS-4 Total'].str.replace(",","")
            mdf['NFHS-4 Total'] = pd.to_numeric(mdf['NFHS-4 Total'])
    else:
        mdf['NFHS-5'] = mdf['NFHS-5'].str.replace(",", "")
        mdf['NFHS-5'] = mdf['NFHS-5'].str.replace("(", "")
        mdf['NFHS-5'] = mdf['NFHS-5'].str.replace(")", "")
        mdf['NFHS-5'] = pd.to_numeric(mdf['NFHS-5'])
        if do_nfhs4:
            mdf['NFHS-4'] = mdf['NFHS-4'].str.replace(",", "")
            mdf['NFHS-4'] = mdf['NFHS-4'].str.replace("(", "")
            mdf['NFHS-4'] = mdf['NFHS-4'].str.replace(")", "")
            mdf['NFHS-4'] = pd.to_numeric(mdf['NFHS-4'])        
    return mdf

def get_state_data(indicators, states):
    mdf = pd.DataFrame()
    for state in states:
        df = pd.read_csv(os.path.join(DATA_PATH, state, 'Indicators.csv'))
        df = df[df['Indicator'].isin([indicators])]
        df['State'] = state
        mdf = mdf.append(df)
    
    #mdf.set_index('State', drop=True, inplace=True)
    if not do_nfhs4:
        return mdf[['State', 'NFHS-5 Rural', 'NFHS-5 Urban', 'NFHS-5 Total']] if not mdf.empty else mdf
    else:
        return mdf[['State', 'NFHS-5 Rural', 'NFHS-5 Urban', 'NFHS-5 Total', 'NFHS-4 Total']] if not mdf.empty else mdf

def get_district_data(indicators, districts_states):
    mdf = pd.DataFrame()
    db = state_dist_to_state_dist_dict(districts_states)
    for state, districts in db.items():
        for district in districts:
            df = pd.read_csv(os.path.join(DATA_PATH, state, district+'.csv'))
            df = df[df['Indicator'].isin([indicators])]
            df['District'] = district + ', ' + state
            mdf = mdf.append(df,)

    #mdf.set_index('District', drop=True, inplace=True)    
    if not do_nfhs4:
        return mdf[['District', 'NFHS-5']] if not mdf.empty else mdf
    else:
        return mdf[['District', 'NFHS-5', 'NFHS-4']] if not mdf.empty else mdf

#------------------------------------------------------------------------------

if len(selected_districts) == 0:
    info = read_state_info(selected_states)
    indicators = build_state_indicators_list(selected_states)
else:
    info = read_district_info(selected_districts)
    indicators = build_district_indicators_list(selected_districts)

#------------------------------------------------------------------------------

indicators_selected = st.selectbox('Indicator', indicators, help='Select an indicator')

#------------------------------------------------------------------------------

if len(selected_districts) == 0:
    data = get_state_data(indicators_selected, selected_states)
else:
    data = get_district_data(indicators_selected, selected_districts)

#------------------------------------------------------------------------------

with st.expander('Sample Data', expanded=True):
    colHH, colW, colM = st.columns(3)
    if info is not None:
        colHH.metric('Households', str(info.sum()['Households']))
        colW.metric('Women', str(info.sum()['Women']))
        colM.metric('Men', str(info.sum()['Men']))

if do_table:
    st.table(data)

if do_chart:
    if len(selected_districts) == 0:
        ax = ["NFHS-5 Rural", "NFHS-5 Urban", "NFHS-5 Total"]
        if do_nfhs4:
            ax = ax + ["NFHS-4 Total"]
        chart = pex.bar(sanitize_data(data), 
                        title=indicators_selected,
                        y="State", 
                        x=ax,
                        text_auto=True,
                        barmode='group',
                        labels={"value":"Value"})
        st.plotly_chart(chart, use_container_width=True, )
    else:
        ax = ["NFHS-5"]
        if do_nfhs4:
            ax = ax + ["NFHS-4"]
        chart = pex.bar(sanitize_data(data),
                        title=indicators_selected,
                        y="District", 
                        x=ax,
                        text_auto=True, 
                        barmode='group',
                        labels={"value":"Value"})
        st.plotly_chart(chart, use_container_width=True)