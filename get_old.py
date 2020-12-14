import requests as r
from bs4 import BeautifulSoup as bs
import pandas as pd
import urllib
import numpy as np
import time
import json
from tqdm import tqdm
from math import ceil
import unicodedata

uri = 'https://www.clarin.com'

def dict_extract(key, var):
    ''' saca value de la key recurrentemente clarin'''
    if hasattr(var,'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in dict_extract(key, v):
                    yield unicodedata.normalize('NFKC',bs(result).text).strip()
            elif isinstance(v, list):
                for d in v:
                    for result in dict_extract(key, d):
                        yield unicodedata.normalize('NFKC',bs(result).text).strip()

class clarin():
    def __init__(self):
        self.url = 'https://www.clarin.com'


    def get(self, url):
        nota = r.get(url)
        sopa = bs(nota.content, features="lxml")
        ps = sopa.find('div', 'body-nota').findAll('p')
        st = sopa.find('div', 'body-nota').findAll('strong')
        self.volanta = sopa.find('p', 'volanta').text
        self.titulo = sopa.find('h1').text
        self.bajada = sopa.find('div', 'bajada').find('h2').text
        texto = list()
        for p in ps:
            if p.text == "COMENTARIOS":
                break
            texto.append(p.text)
        bolds = list()
        for b in st:
            bolds.append(b.text)
        self.cuerpo = ' '.join(texto)
        self.bold = ' '.join(bolds)
        self.bolds = bolds
        self.date = sopa.find('span', {'class': 'publishedDate'}).get_text(strip=True)
        self.get_comments()  
        self.com = ' '.join(self.coms)
    def get_comments(self):
        url=self.url
        url0='https://login.clarin.com/comments.getStreamInfo'
        keys_0={'categoryID': ['Com_03'],
         'APIKey': ['2_fq_ZOJSR4xNZtv2rA8DALl1Gxp7yTYMb3UdER6zerupB55mwkzh9pVBz4Blzi8SW'],
         'sdk': ['js_latest'],
         'authMode': ['cookie'],
         'format': ['jsonp'],
         'callback': ['gigya.callback']}

        keys_0['streamID']=url[-14:-5]
        cm0=r.get(url0,params=keys_0)
        info = json.loads(cm0.text[15:-2])
        N=info['streamInfo']['threadCount']

        keys = {'categoryID': ['Com_03'],
         'includeSettings': ['true'],
         'threaded': ['true'],
         'includeStreamInfo': ['true'],
         'includeUserOptions': ['true'],
         'includeUserHighlighting': ['true'],
         'lang': ['es'],
         'ctag': ['comments_v2'],
         'APIKey': ['2_fq_ZOJSR4xNZtv2rA8DALl1Gxp7yTYMb3UdER6zerupB55mwkzh9pVBz4Blzi8SW'],
         'source': ['showCommentsUI'],
         'sdk': ['js_latest'],
         'authMode': ['cookie'],
         'format': ['jsonp'],
         'callback': ['gigya.callback']}

        keys['streamID']=url[-14:-5]
        coms=[]
        urlcm='https://login.clarin.com/comments.getComments'
        for x in range(ceil(N/10)):    
            req = json.loads(r.get(urlcm,params=keys).text[15:-2])

            #hay replies dentro de replies, busco recursivamente comentarios
            coms.extend(list(dict_extract('commentText', req)))

            #coms.extend([unicodedata.normalize('NFKC',bs(x['commentText']).text) for x in req['comments']])
            #for k in req['comments']:
            #    try: 
            #        coms.extend([unicodedata.normalize('NFKC',bs(rep['commentText']).text) for rep in k['replies']])
            #    except:
            #        pass

            req['comments'][-1]['timestamp']
            keys['start']='ts_'+str(req['comments'][-1]['timestamp'])
        self.coms=coms


months=['01','02','03','04','05','06','07','08','09','10','11','12']

def get_notas(year):
    for m in months:
        url = 'https://www.clarin.com/contents/sitemap_news_' + \
            year + '_' + m + '.xml'
        xml = r.get(url)
        sopa = bs(xml.content, features="lxml")
        urls = [x.get_text() for x in sopa.find_all('loc')]
        notas = []
        fails = []
        for i, x in enumerate(tqdm(urls)):
            nota = clarin()
            try:
                nota.get(x)
                notas.append(nota)
                time.sleep(0.1)
            except:
                fails.append(x)
        data = []
        for l, k in enumerate(notas):
            pupi = list()
            try:
                pupi.append(k.date)
                pupi.append(k.volanta)
                pupi.append(k.bajada)
                pupi.append(k.titulo)
                pupi.append(k.cuerpo)
                pupi.append(k.bold)
                pupi.append(k.com)
                pupi.append(urls[l])
                data.append(pupi)
            except:
                pass
        df = pd.DataFrame(data, columns=[
                          'date', 'volanta', 'bajada', 'titulo', 'cuerpo', 'bold', 'com', 'url'])
        df['cat'] = df.url.apply(lambda x: x.split('/')[3])
        df.to_csv(year + '_' + m +'.csv')
        print('fails: ', len(fails))


def notas(year,month):
    m = month
    url = 'https://www.clarin.com/contents/sitemap_news_' + \
        year + '_' + m + '.xml'
    xml = r.get(url)
    sopa = bs(xml.content, features="lxml")
    urls = [x.get_text() for x in sopa.find_all('loc')]
    notas = []
    fails = []
    for i, x in enumerate(tqdm(urls)):
        nota = clarin()
        try:
            nota.get(x)
            notas.append(nota)
            time.sleep(0.1)
        except:
            fails.append(x)
    data = []
    for l, k in enumerate(notas):
        pupi = list()
        try:
            pupi.append(k.date)
            pupi.append(k.volanta)
            pupi.append(k.bajada)
            pupi.append(k.titulo)
            pupi.append(k.cuerpo)
            pupi.append(k.bold)
            pupi.append(k.com)
            pupi.append(urls[l])
            data.append(pupi)
        except:
            pass
    df = pd.DataFrame(data, columns=[
                        'date', 'volanta', 'bajada', 'titulo', 'cuerpo', 'bold', 'com', 'url'])
    df['cat'] = df.url.apply(lambda x: x.split('/')[3])
    df.to_csv(year + '_' + m +'.csv')
    print('fails: ', len(fails))
