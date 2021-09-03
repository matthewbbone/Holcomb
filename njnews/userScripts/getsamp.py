import time as tm
import pandas as pd
import re
import random as rnd
import click

@click.command(context_settings=dict(ignore_unknown_options=True))
@click.option('--n', default=10, help='The sample size')
@click.option('--datesfile' , default='dates.txt', help='The file that contains a list of target dates')
@click.option('--domainsfile' , default='domains.txt', help='The file that containst a list of target domains')
@click.option('--sourcefile', default='12706-fulltext.txt', help='The source file to extract the sample from')
@click.option('--outputcsv', default='randsamp.csv', help='The output file with the extracted sample')

def get_sample(n, datesfile, domainsfile, sourcefile, outputcsv) -> str:

    chars_to_remove = ",^\()|\""

    start = tm.time()

    datelist = []

    with open(datesfile, 'rb') as dates:

        line = dates.readline()

        while line:
            datelist.append(line.decode('UTF-8')[:-2])
            line = dates.readline()

    domainlist = []

    with open(domainsfile, 'rb') as domains:

        line = domains.readline()
        while line:
            domainlist.append(line.decode('UTF-8')[:-2])
            line = domains.readline()


    # initialize dataframe
    data = pd.DataFrame(columns = ['date','domain','url','text'])
    print(datelist)
    print(domainlist)

    # open 12706-fulltext.txt file for reading
    with open(sourcefile, 'rb') as raw:

        # read first line
        line = raw.readline()
        ctr = 0

        while line:
            
            key = line.decode('UTF-8').split(',', 3)
            key[0] = re.sub('[^0-9]', '', key[0])
            if key[0] in datelist and key[1] in domainlist: 
                data = data.append({'date': key[0], 'domain': key[1], 'url': key[2], 'text': key[3]}, ignore_index=True)      
                
            # read next line
            line = raw.readline()

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
    print('extracted ' + str(len(sample)) + ' articles in ' + str(round(total)) + ' seconds')
    print('ctr: ', ctr)
    print("random sample:")
    print(sample)
    sample.to_csv(outputcsv, index=False)

if __name__ == '__main__':
    get_sample()