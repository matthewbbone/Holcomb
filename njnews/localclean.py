from os import path
from newspaper import Article
import re
import multiprocessing as mp
import pandas as pd
import time as tm

RESULT = []
def overwrite(path):

    ret = {}
    ret['path'] = path

    f = open(path, 'rb')
    article = Article('')
    article.download(f.read())
    if article.download_state != 2:
        print('couldnt parse: ', path)
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
    chosen['cleaned'] = None
    chosen['title'] = None
    chosen['published'] = None
    chosen['author'] = None

    folder= 'chosenSamp'
    results = []
    paths = []

    pool = mp.Pool(mp.cpu_count())

    for index, row in chosen.iterrows():

        path = folder + '/' + ''.join(re.findall('\d+', row.date)) + '_' + ''.join(re.findall('(\d+|[a-zA-Z]+|-|\.)', row.url)) + '.html'
        chosen.loc[index, 'path'] = path
        paths.append(path)

    r = pool.map_async(overwrite, paths)
    r.wait()
    results = r.get()

    res_dict = {}
    for r in results:
        res_dict[r['path']] = r

    ctr = 0

    for index, row in chosen.iterrows():
        
        try:
            chosen.loc[index, 'title'] = res_dict[row.path]['title']
            chosen.loc[index, 'date'] = res_dict[row.path]['date']
            chosen.loc[index, 'text'] = res_dict[row.path]['text']
            try: 
                chosen.loc[index, 'author'] = res_dict[row.path]['author']
            except: ''
        except: 
            ctr = ctr + 1
            print('didnt parse: ', row.path)

    print('errors: ',ctr)
    span = tm.time() - start
    print('completed in ', span, ' seconds')
    chosen.to_csv('parallel_parsed.csv')
    print('length: ', len(results), '  original: ', len(chosen))
    




   