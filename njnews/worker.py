from os import path
from newspaper import Article
import re
import multiprocessing as mp
import pandas as pd
import time as tm

RESULT = []
def overwrite(path):

    ret = {}

    f = open(path, 'rb')
    article = Article('')
    article.download(f.read())
    if article.download_state != 2:
        return ret
    article.parse()


    try:
        ret['path'] = path
        ret['title'] = article.title
        ret['date'] = article.publish_date
        ret['text'] = article.text
        if len(article.authors) > 0: 
            ret['author'] = article.authors[0]
    except:
        print('couldnt parse: ', path)

    return ret

if __name__ == '__main__':

    start = tm.time()

    chosen = pd.read_csv('final_chosen.csv')
    folder= 'chosenSamp'
    results = []
    paths = []

    pool = mp.Pool(mp.cpu_count())

    for index, row in chosen.iterrows():

        path = folder + '/' + ''.join(re.findall('\d+', row.date)) + '_' + ''.join(re.findall('(\d+|[a-zA-Z]+|-|\.)', row.url)) + '.html'
        paths.append(path)

    r = pool.map_async(overwrite, paths)
    r.wait()
    results = r.get()

    span = tm.time() - start
    print('completed in ', span, ' seconds')
    print('lenght: ', len(results))




   