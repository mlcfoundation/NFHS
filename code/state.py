'''
NFHS Data Parser - Extract state data and sampling
Author: Akshay Ranjan <akshay@mlcfoundation.org.in>
MLC Foundation, India
December, 2021
'''

from datetime import date
from multiprocessing import freeze_support, Pool
from time import time
from pandas.core.indexes.base import Index
import pdfplumber
import camelot
import extractor
from utils import time_it
from geo import States
from os import path, stat
import pandas as pd

PATH = path.join('..', 'reports')
DATA_PATH = path.join('..', 'data')

def name_to_path(name):
    return { name: path.join(PATH, name+'.pdf') }

@time_it
def get_info(fmap):
    for name, fname in fmap.items():

        pdf = None
        # Open file
        try:
            pdf = pdfplumber.open(fname)
        except Exception as e:
            return None    

        data = {}

        # The state
        theState = States[name]

        # Determine state parameters
        state_profile = theState['State']['Begin'] + theState['State']['Sample_Info'] - 1
        state_ind = theState['State']['Begin'] + theState['State']['Data_Begin'] - 1
        state_txt = pdf.pages[state_profile].extract_text()
        state_ind_txt = pdf.pages[state_ind].extract_text()
        admin_unit, agency, households, women, men = extractor.extract_info(state_txt, state_ind_txt, None)
        data[admin_unit] = {
            'Agency': agency,
            'Households': households,
            'Women': women,
            'Men': men,
            '_Unit_Name': name,
            '_Unit_File': fname,
            'Districts': {}
        }

        # Determine district parameters
        if theState['Districts'] != 0:
            begin = theState['District']['Begin']
            span = theState['District']['Sample_Info'] + theState['District']['Data_Begin'] + theState['District']['Data_Span'] - 1
            offsets = list(range(begin, span*(theState['Districts']+1), span))

            for offset in offsets:
                district_txt = pdf.pages[offset].extract_text()
                district_ind_txt = pdf.pages[offset+2].extract_text() # A hack!
                district_admin_unit, agency, households, women, men = extractor.extract_info(district_txt, None, district_ind_txt)
                data[admin_unit]['Districts'][district_admin_unit] = {
                    'Agency': agency,
                    'Households': households,
                    'Women': women,
                    'Men': men,
                    '_Unit_Name': district_admin_unit,
                    '_Unit_File': fname,
                    '_Unit_Idx': offset
                }
        #print(json.dumps(data, indent=2))
        return data

@time_it
def get_indicators(info):
    indicators = {}
    for state, state_data in info.items():
        tables = None
        indicators[state] = {}

        # The state
        theState = States[state_data['_Unit_Name']]

        # Get state data span
        d_begin = theState['State']['Begin'] + theState['State']['Data_Begin']
        d_end = d_begin + theState['State']['Data_Span'] - 1

        # Open file in camelot
        try:
            tables = camelot.read_pdf(state_data['_Unit_File'], 
                                      f'{d_begin}-{d_end}',
                                      flavor='stream',
                                      flag_size=True,
                                      strip_text='\n',
                                      row_tol=10,
                                      layout_kwargs={'detect_vertical': False},
                                      table_areas=['31,800,560,50'])
        except Exception as e:
            return e

        # Determine state data
        indicators[state]['State'] = \
            extractor.extract_state_data(tables, state_data['_Unit_Name'])

        # Determine district data
        if theState['Districts'] != 0:
            indicators[state]['Districts'] = []
            for district, district_data in state_data['Districts'].items():
                d_begin = district_data['_Unit_Idx'] + theState['District']['Data_Begin']
                d_end = d_begin + theState['District']['Data_Span'] - theState['District']['Data_Begin']

                # Open file in camelot
                tables = camelot.read_pdf(state_data['_Unit_File'], 
                                          f'{d_begin}-{d_end}',
                                          flavor='stream',
                                          flag_size=True,
                                          strip_text='\n',
                                          row_tol=10,
                                          layout_kwargs={'detect_vertical': False},
                                          table_areas=['31,775,560,50'],
                                          columns=['470,523'])

                # Determine district data
                indicators[state]['Districts'].append({
                    district: extractor.extract_districts_data(tables, district)
                })
    return indicators

def get_state_info(info):
    for state, data in info.items():
        return { 
            'State': state,
            'Agency': data['Agency'],
            'Households': data['Households'],
            'Women': data['Women'],
            'Men': data['Men']
        }

def get_district_info(info):
    for state, data in info.items():
        return {
            state: data['Districts']
        }

@time_it
def persist_sampling(samplings):
    df = pd.DataFrame(samplings)
    df.to_csv(path.join(DATA_PATH, 'SampleInfo.csv'), index=False)

@time_it
def persist_districts_sampling(samplings):
    for sample in samplings:
        for state, districts in sample.items():
            data = []
            for district, info in districts.items():
                data.append({
                    'District': district,
                    'Agency': info['Agency'],
                    'Households': info['Households'],
                    'Women': info['Women'],
                    'Men': info['Men']
                })
            df = pd.DataFrame(data)
            df.to_csv(path.join(DATA_PATH, state, 'SampleInfo.csv'), index=False)

@time_it
def persist_indicators(indicators):
    for state_indicators in indicators:
        for state, state_data in state_indicators.items():
            state_data['State'].to_csv(path.join(DATA_PATH, state, 'Indicators.csv'), index=False)

@time_it
def persist_districts_indicators(indicators):
    for state_indicators in indicators:
        for state, state_data in state_indicators.items():
            if 'Districts' in state_data:
                for district_indicators in state_data['Districts']:
                    for district, district_data in district_indicators.items():
                        district_data.to_csv(path.join(DATA_PATH, state, district+'.csv'), index=False)
            else:
                print(f'...No districts in {state}')

@time_it
def main():
    with Pool(processes=6) as mp:
        fmaps = mp.map(name_to_path, States.keys()) #[ name_to_path(state) for state in States.keys() ]
        info = mp.map(get_info, fmaps) #[ extract_sampling(fmap) for fmap in fmaps ]
        indicators = mp.map(get_indicators, info)
        state_info = mp.map(get_state_info, info)
        district_info = mp.map(get_district_info, info)

    persist_sampling(state_info)
    persist_districts_sampling(district_info)
    persist_indicators(indicators)
    persist_districts_indicators(indicators)

if __name__ == '__main__':
    freeze_support()
    main()