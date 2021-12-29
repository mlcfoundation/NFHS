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

# Careful with the following table as its manually determined
COMMON_ROWS = [45,98,99,100,154,186]
DISCARD_ROWS = {
    'Jammu_Kashmir': COMMON_ROWS,
    'Punjab': COMMON_ROWS
}

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

    print(f'Extracted data for {name}')
    return df

def extract_districts_data(tables, name):
    pass

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
        match = re.search('^(?P<district>.*?)\,\s+(?P<state>.*?)(\-|\–) (.*?)$', lines[0]+lines[1], re.DOTALL)
        if match is not None:
            admin_unit = match.group('district').strip()
            #print(f'DISTRICT: {admin_unit}')

    '''
    # Match to find state or district name
    #match = re.search('[trends|indicators]\s+for\s+(?P<ADMIN_UNIT>.*?).\s+NFHS-5\s+fieldwork', txt, re.DOTALL|re.UNICODE)
    #match = re.search('fieldwork\s+for\s+(?P<ADMIN_UNIT>.*?)\s+was\s+conducted\s+from', txt, re.DOTALL)
    match = re.search('This\s+fact\s+sheet\s+provides\s+information\s+on\s+key\s+indicators\s+and\s+trends\s+for\s+(?P<ADMIN_UNIT>.*?)\.', txt, re.DOTALL)
    if match is not None:
        admin_unit = match.group('ADMIN_UNIT').strip().replace('\n', '')
    else:
        match = re.search('This\s+fact\s+sheet\s+provides\s+information\s+on\s+key\s+indicators\s+for\s+(?P<ADMIN_UNIT>.*?)\.', txt, re.DOTALL)
        if match is not None:
            admin_unit = match.group('ADMIN_UNIT').strip().replace('\n', '')
    '''
    return admin_unit, agency, households, women, men

