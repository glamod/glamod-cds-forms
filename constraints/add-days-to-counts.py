#!/usr/bin/env python

"""
Adds a "day" column to a counts file, given as the only
command-line parameter. 

Also writes a backup ".bak" file just in case.
"""

import shutil
import sys
import calendar

import pandas as pd



def parse_counts(counts_file): 
    df = pd.read_csv(counts_file, dtype=str, skipinitialspace=True)
    return df


def main(counts_file=sys.argv[1]):

    df = parse_counts(counts_file)
    columns = list(df.columns)
    columns.insert(-1, 'day')

    data = []
    header = True
    mode = 'w'

    counts_new = f'{counts_file}.days'

    for _, row in df.iterrows():

        if _ > 0 and _ % 1000 == 0: 
            print(f'Progress: {_} out of {len(df)}')

        n_days = calendar.monthrange(int(row.year), int(row.month))[1]
         
        for i in range(1, n_days + 1):
            _row = row.copy()         
            _row['day'] = f'{i:02d}'
            data.append(_row)

        if len(data) > 10000:
            chunk = pd.DataFrame(data=data, columns=columns) 
            chunk.to_csv(counts_new, columns=columns, mode=mode, header=header, index=False)
            header = False

            mode = 'a'
            print(f'Wrote {len(chunk)} records so far...')
            data = []
                
    print(f'Wrote: {counts_new}') 


if __name__ == '__main__':

    main()
