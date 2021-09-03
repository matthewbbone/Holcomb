from newspaper import Article
from datetime import datetime as dt
import multiprocessing as mp
import pandas as pd
import time as tm
import requests
from bs4 import BeautifulSoup

RESULT = []
def overwrite(info):

    ret = {}
    ret['url'] = info[1]

    if info[1] is None:
        print('no matching webpage')
        return ret
    article = Article(info[1])
    article.download()
    if article.download_state != 2:
        print('couldnt parse: ', info[1])
        return ret
    article.parse()

    try:
        ret['index'] = info[0]
        ret['title'] = article.title
        ret['date'] = article.publish_date
        ret['text'] = article.text
        if len(article.authors) > 0: 
            ret['author'] = ';'.join(article.authors)
        else:
            ret['author'] = None
    except:
        print('couldnt parse: ', info[1])

    return ret

def scrape_home(info):  

    target_url = None
    ret = {}
    ret['url'] = info[1]

    page = requests.get(info[1])
    soup = BeautifulSoup(page.content, "lxml")
    alist = soup.find_all("a")
    alist = [a for a in alist if 'onclick' in a.attrs]
    
    for a in alist:
    
        if dt.strptime(a.text, '%b %d, %Y') == dt.strptime(info[2], '%Y-%m-%d'):
            target_url= a.attrs['href']

    if target_url is None:
        print('no matching webpage')
        return ret
    article = Article(target_url)
    article.download()
    if article.download_state != 2:
        print('couldnt parse: ', target_url)
        return ret
    article.parse()

    try:
        ret['index'] = info[0]
        ret['title'] = article.title
        ret['date'] = article.publish_date
        ret['text'] = article.text
        if len(article.authors) > 0: 
            ret['author'] = ';'.join(article.authors)
        else:
            ret['author'] = None
    except:
        print('couldnt parse: ', target_url)

    return ret

    

if __name__ == '__main__':

    start = tm.time()

    # 10: 11
    # 50: 78
    # 100: 85
    # 200: 71
    # 500: 187
    # 1000: 325
    # 2000: 577
    #
    # w/o Social Media
    # 10: 4
    # 50: 17
    # 100: 30
    # 200: 54
    # 500: 122
    # 1000: 256
    # 2000: 500
    chosen = pd.read_csv('randsamp.csv')
    chosen['title'] = None
    chosen['published'] = None
    chosen['author'] = None
    chosen['clean_text'] = None

    ai_url = "https://wayback.archive-it.org"
    collection_id=12706
    home_list = []
    url_list = []
    results = []

    for index, row in chosen.iterrows():

        home = ai_url + '/' + str(collection_id) + '/*/' + row.url
        chosen.loc[index, 'url'] = home
        home_list.append([index, home, row.date])

    search_pool = mp.Pool(mp.cpu_count())
    s = search_pool.map_async(scrape_home, home_list)
    s.wait()
    results = s.get()
        
    res_dict = {}
    for r in results:
        try:
            res_dict[r['index']] = r
        except Exception as e: ''

    ctr = 0

    for index, row in chosen.iterrows():
        
        try:
            chosen.loc[index, 'title'] = res_dict[index]['title']
            chosen.loc[index, 'published'] = res_dict[index]['date']
            chosen.loc[index, 'clean_text'] = res_dict[index]['text']
            try: 
                chosen.loc[index, 'author'] = res_dict[index]['author']
            except: ''
        except: ''

    span = tm.time() - start
    print('completed in ', span, ' seconds')
    print(chosen)
    chosen.to_csv('pp_fe.csv')
    print('length: ', len(res_dict), '  original: ', len(chosen))
    print('errors: ', len(chosen) - len(res_dict))
    




   