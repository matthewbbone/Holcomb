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
            ret['author'] = article.authors[0]
    except:
        print('couldnt parse: ', info[1])

    return ret

def scrape_home(info):  

    ret = {}

    page = requests.get(info[1])
    soup = BeautifulSoup(page.content, "lxml")
    alist = soup.find_all("a")
    alist = [a for a in alist if 'onclick' in a.attrs]
    
    for a in alist:
    
        if dt.strptime(a.text, '%b %d, %Y') == dt.strptime(info[2], '%Y-%m-%d'):
            ret['index'] = info[0]
            ret['url'] = 'https:' + a.attrs['href']
    
    return ret

    

if __name__ == '__main__':

    start = tm.time()

    chosen = pd.read_csv('final_chosen.csv')
    chosen['title'] = None
    chosen['published'] = None
    chosen['author'] = None

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
    info_list = s.get()
    url_list = [[i['index'], i['url']] for i in info_list]
    print('Webscraped in ', tm.time() - start, ' seconds')

    parse_pool = mp.Pool(mp.cpu_count())
    p = parse_pool.map_async(overwrite, url_list)
    p.wait()
    results = p.get()
    
    res_dict = {}
    for r in results:
        try:
            res_dict[r['index']] = r
        except: ''

    ctr = 0

    for index, row in chosen.iterrows():
        
        try:
            chosen.loc[index, 'title'] = res_dict[index]['title']
            chosen.loc[index, 'date'] = res_dict[index]['date']
            chosen.loc[index, 'text'] = res_dict[index]['text']
            try: 
                chosen.loc[index, 'author'] = res_dict[index]['author']
            except: ''
        except Exception as e:
            ctr = ctr + 1
            print('didnt parse: ', row.url)

    print('errors: ',ctr)
    span = tm.time() - start
    print('completed in ', span, ' seconds')
    chosen.to_csv('pp_fe.csv')
    print('length: ', len(res_dict), '  original: ', len(chosen))
    




   