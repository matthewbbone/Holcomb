import time as tm
from numpy.lib.utils import source
import pandas as pd
import re
import random as rnd
import click

@click.command(context_settings=dict(ignore_unknown_options=True))
@click.option('--n', default=10, help='The sample size (def: 10)')
@click.option('--datesfile' , default='dates.txt', help='File that has a list of dates (def: dates.txt)')
@click.option('--domainsfile' , default='domains.txt', help='File that has a list of domains (def: domains.txt)')
@click.option('--sourcefile', default='12706-fulltext.txt', help='Raw text file (def: 12706-fulltext.txt)')
@click.option('--outputcsv', default='randsamp.csv', help='File to output the sample (def: randsamp.csv)')

def get_sample(n, datesfile, domainsfile, sourcefile, outputcsv) -> str:

    chars_to_remove = ",^\()|\""

    start = tm.time()

    datelist = []

    print('parsing', datesfile, '...')
    with open(datesfile, 'rb') as dates:

        line = dates.readline()

        while line:
            datelist.append(line.decode('UTF-8'))
            line = dates.readline()

    datelist = [date[:-2] for date in datelist][:-1] + [datelist[-1]]

    domainlist = []

    print('parsing', domainsfile, '...')
    with open(domainsfile, 'rb') as domains:

        line = domains.readline()
        while line:
            domainlist.append(line.decode('UTF-8'))
            line = domains.readline()

    domainlist = [domain[:-2] for domain in domainlist][:-1] + [domainlist[-1]]

    # initialize dataframe
    data = pd.DataFrame(columns = ['date','domain','url','text'])

    print('extracting from', sourcefile, '...')
    # open 12706-fulltext.txt file for reading
    with open(sourcefile, 'rb') as raw:

        # read first line
        # line = raw.readline()
        ctr = 0

        for line in raw:
            
            key = line.decode('UTF-8').split(',', 3)
            key[0] = re.sub('[^0-9]', '', key[0])
            if key[0] in datelist and key[1] in domainlist: 
                data = data.append({'date': key[0], 'domain': key[1], 'url': key[2], 'text': key[3]}, ignore_index=True)      
                
            # read next line
            # line = raw.readline()

            ctr = ctr + 1

    # take time difference
    total = tm.time() - start

    # remove problematic characters from text
    text = [s.translate ({ord(c): "" for c in chars_to_remove}) for s in data['text']]
    # take off trailing /
    url = [s.strip('/') for s in data['url']]
    # replace old text with cleaned text
    data = data.assign(text = text).assign(url = url)
    # convert date to standard format
    data['date'] = pd.to_datetime(data['date'])

    if n < len(data):
        sample = data.sample(n)
    else:
        sample = data

    print("random sample:")
    print(sample)
    print('extracted', str(len(sample)), 'articles in', str(round(total)), 'seconds')
    print('lines searched:', ctr)
    print('output to:', outputcsv)
    sample.to_csv(outputcsv, index=False)

if __name__ == '__main__':
    get_sample()