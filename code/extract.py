'''

NFHS5 Data Parser

Author: Akshay Ranjan <akshay@mlcfoundation.org.in>

MLC Foundation, India

December, 2021

'''
from geo import States, UTs
from os.path import exists
from os import mkdir, getpid
from multiprocessing import Pool, freeze_support

import urllib.request
import re # Regular Expressions
import camelot # PDF table extrator based on tabula
import pdfplumber # PDF parser
import pandas # Pandas
import functools
import time
import hashlib


# Location of data
URI = 'http://rchiips.org/nfhs/NFHS-5_FCTS/COMPENDIUM/'

# Download location
DOWNLOADS = './../reports/'

# Data location
DATA = './../data/'

# Page offset
PAGE_OFFSET = 12

# Time code
def time_it(func):
    @functools.wraps(func)
    def timed_func(*args, **kwargs):
        st = time.perf_counter()
        val = func(*args, **kwargs)
        et = time.perf_counter()
        run_time = et - st
        print(f"[{getpid()}] {func.__name__!r} took {run_time:.4f}")
        return val
    return timed_func

# Download files
@time_it
def download_pdf(fname):
    URL = URI+fname+".pdf"
    fname = DOWNLOADS+fname+".pdf"
    
    print(f'[{getpid()}] Downloading {fname}')
    
    if exists(fname) == False:

        dfname, headers = urllib.request.urlretrieve(URL, fname)
    return fname

# Parse the PDF
@time_it
def parse_state(fname):
    print(f"[{getpid()}] Parsing {fname}")

    # Use pdfplumber to parse text
    try:
        pdf = pdfplumber.open(fname)
    except:
        pass

    # Real useful text starts from page PAGE_OFFSET onwards
    pages = pdf.pages[PAGE_OFFSET:len(pdf.pages)]
    
    # Districts table location dictionary
    districts = {}

    # State
    state = None

    # Build dictionary of districts
    for page_num, page in enumerate(pages):
        # Extract text
        txt = page.extract_text()
        
        # Convert text to lines (using CRLF/LF)
        lines = txt.strip().split('\n')

        # Skip pages containing non-data text
        if lines[0].strip() == 'NOTES' or \
           lines[0].strip() == 'Ministry of Health and Family Welfare' or \
           lines[0].strip() == 'Introduction' or \
           lines[0].strip() == 'INTERNATIONAL INSTITUTE FOR POPULATION SCIENCES' or \
           len(lines) == 0 or \
           txt.isnumeric():
           continue

        # Parse district name and state name
        try:
            # Special case for Dadra & Nagar Haveli
            if lines[0][:5] == 'Dadra':
                match = re.search("^(?P<district>.*?)\, (?P<state>.*?)(\-|\–) (.*?)$", lines[0]+lines[1])
            else:
                match = re.search("^(?P<district>.*?)\, (?P<state>.*?)(\-|\–) (.*?)$", lines[0].strip())
            district = match.group('district').strip()
            state = match.group('state').strip()
        except:
            district = 'eD'
            state = 'eS'

        # Update dictionary
        if district not in districts.keys():
            districts[district] = [page_num + PAGE_OFFSET]
        else:
            districts[district].append((page_num + PAGE_OFFSET))
    
    print(f"[{getpid()}] Parsed PDF for {state}")
    
    return (state, districts, fname)

# Extract tables from a page
@time_it
def extract_tables(district_name, page, fname):
    df = None

    print(f"[{getpid()}] Extracting table from [{page}] in PDF for {district_name}")

    # Extract tables
    try:
        tables = camelot.read_pdf(fname,
                                  pages=str(page+1),
                                  flavor='stream',
                                  strip_text='\n',
                                  flag_size=True,
                                  layout_kwargs={'detect_vertical': False})
    except:
        pass

    print(f"[{getpid()}] Extracted {len(tables)} tables for {district_name}")

    if len(tables) == 2:
        df = tables[0].df
    elif len(tables) == 3:
        df = tables[1].df
    else:
        return pandas.DataFrame()

    num_cols = len(df.columns)

    if num_cols == 2: # For only NFHS5 data
        df.columns=['Indicator','NFHS_5']
    elif num_cols == 3: # For NFHS4/5 data
        df.columns=['Indicator','NFHS_5', 'NFHS_4']
    elif num_cols > 3: # In some cases, camelot is inserting a spurious column, drop that col
        print(f"[{getpid()}] Dropping extraneous column from table for {district_name}")
        df.drop(df.columns[[3]], axis=1, inplace=True)
        df.columns=['Indicator','NFHS_5', 'NFHS_4']

    # Drop first two rows
    df.drop(labels=[0,1], inplace=True)

    # Fix datatypes
    df.convert_dtypes()

    return df

# Extract all tables from pages relevant to a district
@time_it
def parse_table(district, fname):
    district_name = district[0]
    page_list     = district[1]
    df            = pandas.DataFrame()
    
    print(f"[{getpid()}] Parsing pages [{page_list}] in PDF for {district_name}")

    # Extract tables
    dfs = [extract_tables(district_name, page_num, fname) for page_num in page_list]

    # Merge all data frames
    for idx in range(len(dfs)):
        df = df.append(dfs[idx], ignore_index=True)
    
    # Meta categories
    categories = {}
    # Rows that need to be appended
    appends = {}
    # Rows that need to be dropped
    drops = {}

    # Cleanup rows in data frame
    for row in df.itertuples():
        try:
            if row[1][0].strip().isdigit():
                # Knock off the bullet list number
                df.at[row[0], 'Indicator'] = row[1].split('.',1)[1].strip()
            elif row[1][0].isupper():
                if row[0] not in categories:
                    categories[row[0]] = row[1]
                    if row[1].strip() == 'Men' or row[1].strip() == 'Women':
                        appends[row[0]] = row[1]
                    drops[row[0]] = {}
            elif row[1][0].islower():
                df.at[row[0], 'Indicator'] = df.at[row[0]-1, 'Indicator'] + ' ' + df.at[row[0], 'Indicator']
                drops[row[0]-1] = {}
        except:
            print(row)

        # camelot adds <s></s> tags for subscripted text, remove them here
        df.at[row[0], 'Indicator'] = re.sub("\<s\>(.*?)<\/s\>", "", df.at[row[0], 'Indicator'])
    
    # Do all appends (this is required for text that spills over next row)
    for row_id in appends.keys():
        for next_row_id in range(1,5):
            df.at[row_id+next_row_id, 'Indicator'] = appends[row_id] + " - " + df.at[row_id+next_row_id, 'Indicator']
    
    # Do all drops
    for row_id in drops.keys():
        df.drop(row_id, inplace=True)
 
    return (district_name, df)

@time_it
def parse_district(state): 
    state_name  = state[0]
    districts   = state[1]
    state_fname = state[2]

    print(f"[{getpid()}] Parsing {state_name} for {len(districts)} districts")
    
    # District table data frames
    district_dfs = [parse_table(district, state_fname) for district in districts.items()]

    return (state_name, district_dfs)

# Create district file
@time_it
def create_district_file(state_name, district):
    district_name = district[0]
    df = district[1]

    print(f"[{getpid()}] Writing CSV for {state_name}, {district_name}")

    # Put files in respective dirs
    if not exists(DATA+state_name):
        mkdir(DATA+state_name)
    
    # Write CSV files
    try:
        fname = DATA+state_name+'/'+district_name+'.csv'
        df.to_csv(fname)
    except:
        pass

    return (state_name, district_name, fname)

# Verify district file
def verify_district_file(fname):
    lines = 0
    with open(fname, 'r') as f:
        lines = f.readlines()
    return len(lines)

# Checksum district file
@time_it
def csum_district_file(district):
    state_name = district[0]
    district_name = district[1]
    fname = district[2]
    lines = district[3]
    csum = None

    with open(fname, 'rb') as f:
        bytes = f.read()
        csum =  hashlib.sha3_256(bytes).hexdigest()

    return (state_name, district_name, fname, lines, csum)

# Create files
@time_it
def create_and_csum_files(district):
    state_name = district[0]
    districts = district[1]

    # Create files
    data_files = [create_district_file(state_name, district) for district in districts]

    '''
    # Verify files
    verified_files = [verify_district_file(district) for district in districts]
    
    # Checksum files
    csum_files = list(map(csum_district_file, verified_files))
    '''
    
    return data_files

@time_it
def main():
    with Pool() as mp:
        files = list(mp.map(download_pdf, UTs))
        states = list(mp.map(parse_state, files, chunksize=1))
        districts = list(mp.map(parse_district, states, chunksize=1))
        data_files = list(mp.map(create_and_csum_files, districts, chunksize=1))

    for state in data_files:
        for district in state:
            lines = verify_district_file(district[2])
            if lines != 105:
                print(f"[{getpid()}] Unfaithful extraction (105:{lines}) from {district[2]} for {district[0]}, {district[1]}")


if __name__ == '__main__':
    freeze_support()
    main()