from os import path, scandir
from multiprocessing import Pool, freeze_support
import csv

DATA_PATH = path.join('..', 'data')
EXPECTED_STATE_INDICATORS_LEN = 132
EXPECTED_DISTRICT_INDICATORS_LEN = 105

def validate_file(fname):
    with open(fname, 'r') as f:
        num_lines = len(f.readlines())

        if fname.endswith('Indicators.csv'):
            if num_lines > EXPECTED_STATE_INDICATORS_LEN:
                print(f"{fname} = {num_lines} EXPECTED={EXPECTED_STATE_INDICATORS_LEN}")
                return {fname: num_lines}
        elif fname.endswith('SampleInfo.csv'):
            return {fname: 0}
        else:
            if num_lines > EXPECTED_DISTRICT_INDICATORS_LEN:
                print(f"{fname} = {num_lines} EXPECTED={EXPECTED_DISTRICT_INDICATORS_LEN}")
                return {fname: num_lines}            

def main():
    path_v = []
    results = []
    with scandir(DATA_PATH) as it:
        for entry in it:
            if entry.is_dir():
                with scandir(entry.path) as fit:
                    for fentry in fit:
                        if fentry.is_file():
                            path_v.append(fentry.path)

    with Pool(processes=6) as mp:
        results = mp.map(validate_file, path_v)


if __name__ == '__main__':
    freeze_support()
    main()