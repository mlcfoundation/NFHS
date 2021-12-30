'''
NFHS Data Parser - Extract state sampling information
Author: Akshay Ranjan <akshay@mlcfoundation.org.in>
MLC Foundation, India
December, 2021
'''

import pdfplumber
import camelot
import re
import pandas as pd

INDICATOR_STATE_PREFIX_WOMEN_ROWS = [98,99,100,104,105,106,110,111,112]
INDICATOR_STATE_PREFIX_MEN_ROWS = [101,102,103,107,108,109,113]
INDICATOR_DISTRICT_PREFIX_WOMEN_ROWS = [85,86,87,91,92,93]
INDICATOR_DISTRICT_PREFIX_MEN_ROWS = [88,89,90,94,95,96]

def extract_state_data(tables, name):
    df = pd.DataFrame()

    # Merge tables
    for table in tables:
        # Drop few two rows
        table.df.drop(labels=[0,1], inplace=True)
        # Add new column headers
        table.df.columns = ['Indicator', 'NFHS-5 Urban', 'NFHS-5 Rural', 'NFHS-5 Total', 'NFHS-4 Total']
        # Append table
        df = df.append(table.df, ignore_index=True)
    
    # Reindex
    df.reset_index(drop=True, inplace=True)

    droppable = []
    for row in df.itertuples():
        if (row[1].strip().startswith('<s>')) or \
           (len(row[1].strip()) == 0) or \
           (len(row[4].strip()) == 0) or \
           (row[2].strip().startswith('Urban') and row[3].strip().startswith('Rural')):
                droppable.append(row[0])

    # Drop all dropeables
    df.drop(labels=list(droppable), inplace=True)

    # Reindex
    df.reset_index(drop=True, inplace=True)

    for row in df.itertuples():
        # camelot adds <s></s> tags for subscripted text, remove them here
        df.at[row[0], 'Indicator'] = re.sub("\<s\>(.*?)\<\/s\>", "", df.at[row[0], 'Indicator'], re.DOTALL)
        # remove the numbered list from indicators
        df.at[row[0], 'Indicator'] = re.sub("^\d+\.[\s+]?", "", df.at[row[0], 'Indicator'])

        if row[0] in INDICATOR_STATE_PREFIX_WOMEN_ROWS:
            df.at[row[0], 'Indicator'] = 'Women - ' + df.at[row[0], 'Indicator']
        elif row[0] in INDICATOR_STATE_PREFIX_MEN_ROWS:
            df.at[row[0], 'Indicator'] = 'Men - ' + df.at[row[0], 'Indicator']        

    print(f'Extracted data for {name}')
    return df

def extract_districts_data(tables, name):
    df = pd.DataFrame()
    
    # Merge tables
    for table in tables:
        # Since we are manually specifying the column boundaries, even the 
        # tabels having only NFHS-5 data are gong to have 3 columns. We need
        # drop that column.
        if table.df.iat[0,2].strip().startswith('NFHS-5'):
            table.df.drop(columns=[1], inplace=True)
        # Drop few two rows
        table.df.drop(labels=[0,1], inplace=True)
        # Add new column headers
        table.df.columns = ['Indicator', 'NFHS-5', 'NFHS-4'] if len(table.df.columns) == 3 else ['Indicator', 'NFHS-5']        
        # Append table
        df = df.append(table.df, ignore_index=True)
    
    # Reindex
    df.reset_index(drop=True, inplace=True)

    # Number of columns
    num_cols = len(df.columns)

    droppable = []
    for row in df.itertuples():
        if num_cols == 2:
            # For districts that are newly created between NFHS4 and NFHS5
            # time period.
            if (str(row[1]).strip().startswith('<s>')) or \
                (len(str(row[1]).strip()) == 0) or \
                (len(str(row[2]).strip()) == 0) or \
                (str(row[2]).strip().startswith('Total')):
                    droppable.append(row[0])            
        else:
            if (str(row[1]).strip().startswith('<s>')) or \
                (len(str(row[1]).strip()) == 0) or \
                (len(str(row[3]).strip()) == 0) or \
                (str(row[2]).strip().startswith('Total') and str(row[3]).strip().startswith('Total')):
                    droppable.append(row[0])

    # Drop all dropeables
    df.drop(labels=list(droppable), inplace=True)

    # Reindex
    df.reset_index(drop=True, inplace=True)

    for row in df.itertuples():
        # camelot adds <s></s> tags for subscripted text, remove them here
        df.at[row[0], 'Indicator'] = re.sub("\<s\>(.*?)\<\/s\>", "", df.at[row[0], 'Indicator'], re.DOTALL)
        # remove the numbered list from indicators
        df.at[row[0], 'Indicator'] = re.sub("^\d+\.[\s+]?", "", df.at[row[0], 'Indicator'])

        if row[0] in INDICATOR_DISTRICT_PREFIX_WOMEN_ROWS:
            df.at[row[0], 'Indicator'] = 'Women - ' + df.at[row[0], 'Indicator']
        elif row[0] in INDICATOR_DISTRICT_PREFIX_MEN_ROWS:
            df.at[row[0], 'Indicator'] = 'Men - ' + df.at[row[0], 'Indicator']

    print(f'...Extracted data for {name}')
    return df

def extract_info(txt, state_ind_txt, district_ind_txt):
    # Params we are looking for
    agency = None
    households = 0
    women = 0
    men = 0
    admin_unit = None

    # Match to find sampling agency name
    match = re.search('by\s+(?P<AGENCY>.*?)\.\s+In', txt, re.UNICODE | re.DOTALL)
    if match is not None:
        agency = match.group('AGENCY').replace('\n','')
    
    # Match to find sample size
    match = re.search('from\s+(?P<H>.*?)\s+households,\s+(?P<W>.*?)\s+women,\s+and\s+(?P<M>.*?)\s+men', txt)
    if match is not None:
        households = int(match.group('H').replace(',','').strip())
        women = int(match.group('W').replace(',','').strip())
        men = int(match.group('M').replace(',','').strip())

    if state_ind_txt is not None:
        lines = state_ind_txt.strip().split('\n')
        match = re.search('^(?P<state>.*?)(\-|\–) (.*?)$', lines[0]+lines[1], re.DOTALL)
        if match is not None:
            admin_unit = match.group('state').strip()
            #print(f'STATE: {admin_unit}')
    elif district_ind_txt is not None:
        lines = district_ind_txt.strip().split('\n')
        if lines[0].strip().startswith('Sikar'):
            admin_unit = lines[0].strip().split()[0]
            print(f'DISTRICT: {admin_unit}')
        else:
            match = re.search('^(?P<district>.*?)\,\s+(?P<state>.*?)(\-|\–) (.*?)$', lines[0]+lines[1], re.DOTALL)
            if match is not None:
                admin_unit = match.group('district').strip()
                #print(f'DISTRICT: {admin_unit}')

    return admin_unit, agency, households, women, men

