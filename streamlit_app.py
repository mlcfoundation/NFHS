'''

Sample script to visualize NFHS5 data using streamlit.io

Akshay Ranjan <akshay@mlcfoundation.org.in>

'''
from numpy import modf
import streamlit as st
import pandas as pd
import numpy as np
import os
import csv

DATA_PATH = os.path.join('.', 'data')

st.title('NFHS5 Data Comparison')

#------------------------------------------------------------------------------
def build_states_list():
    states = []
    for fe in os.scandir(DATA_PATH):
        if fe.is_dir():
            states.append(fe.name)
    return states
states = build_states_list()
selected_states = st.multiselect('Select state', states)

#------------------------------------------------------------------------------
def build_districts_list(states):
    data = {}
    districts = []
    for state in states:
        for fe in os.scandir(os.path.join(DATA_PATH, state)):
            if fe.is_file():
                name = fe.name.split('.')[0]
                data[name] = state
                districts.append(name)
    return data, districts
states_districts, districts = build_districts_list(selected_states)
selected_districts = st.multiselect('Select districts', states_districts)

#------------------------------------------------------------------------------
def read_data(districts):
    global states_districts
    data = {}
    indicators = {}

    for se in districts:
        state = states_districts[se]
        path = os.path.join(DATA_PATH, state, se+".csv")
        df = pd.read_csv(path, delimiter=",")
        data[se] = (state, df)
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
indicator_selected = st.selectbox('Select indicator', indicators)

#------------------------------------------------------------------------------
def format_data(indicator, data):
    mdf = pd.DataFrame()
    if len(data):
        for de in data.items():
            df = de[1][1].loc[de[1][1]['Indicator'] == indicator ][['Indicator','NFHS_5']]
            df['State'] = de[1][0]
            df['District'] = de[0]
            mdf = mdf.append(df)
        mdf = mdf.pivot(index=['State','District'], values='NFHS_5', columns='Indicator').reset_index()
    return mdf
mdata = format_data(indicator_selected, data)
#st.bar_chart(mdata)
st.table(mdata)

        



    

