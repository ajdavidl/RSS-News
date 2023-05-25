import feedparser
import pandas as pd
import re
from datetime import datetime
import time
import string

NITTER_URL = "https://nitter.net/"


def strip_html_tags(text):
    p = re.compile(r'<.*?>')
    return p.sub('', text)


def remove_url(string):
    if type(string) != str:
        return(string)
    return(re.sub(r'http\S+', '', string))


def strip_all_entities(text):
    if type(text) != str:
        return(text)
    text = re.sub('“', '', text)
    text = re.sub('”', '', text)
    text = re.sub('"', '', text)
    entity_prefixes = ['@', '#']
    for separator in string.punctuation:
        if separator not in entity_prefixes:
            text = text.replace(separator, ' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)


def remove_numeros(string):
    if type(string) != str:
        return(string)
    string = re.sub('[0-9]+', '', string)
    return(string)


def limpa_url(url):
    url = re.sub('https://', '', url)
    url = re.sub('http://', '', url)
    url = re.sub('www1.', '', url)
    url = re.sub('www.', '', url)
    url = url.split("/")[0]
    url = re.sub('.com.br', '', url)
    url = re.sub('.com', '', url)
    url = re.sub('\.', ' ', url)
    return url


def translateDate(txtDate):
    txtDate = re.sub('Fev', 'Feb', txtDate)
    txtDate = re.sub('Abr', 'Apr', txtDate)
    txtDate = re.sub('Mai', 'May', txtDate)
    txtDate = re.sub('Ago', 'Aug', txtDate)
    txtDate = re.sub('Set', 'Sep', txtDate)
    txtDate = re.sub('Out', 'Oct', txtDate)
    txtDate = re.sub('Dez', 'Dec', txtDate)

    txtDate = re.sub('Seg', 'Mon', txtDate)
    txtDate = re.sub('Ter', 'Tue', txtDate)
    txtDate = re.sub('Qua', 'Wed', txtDate)
    txtDate = re.sub('Qui', 'Thu', txtDate)
    txtDate = re.sub('Sex', 'Fri', txtDate)
    txtDate = re.sub('Sáb', 'Sat', txtDate)
    txtDate = re.sub('Dom', 'Sun', txtDate)

    txtDate = re.sub('seg', 'Mon', txtDate)
    txtDate = re.sub('ter', 'Tue', txtDate)
    txtDate = re.sub('qua', 'Wed', txtDate)
    txtDate = re.sub('qui', 'Thu', txtDate)
    txtDate = re.sub('sex', 'Fri', txtDate)
    txtDate = re.sub('sáb', 'Sat', txtDate)
    txtDate = re.sub('dom', 'Sun', txtDate)
    return txtDate


def retorna_noticias(url):
    usuarios = []
    textos = []
    datas = []
    titulos = []
    links = []
    try:
        NewsFeed = feedparser.parse(url)
        for d in NewsFeed.entries:
            titulos.append(d['title'])
            links.append(d['link'])
            if NITTER_URL in url:
                usuarios.append(d['author'])
            elif "newsbrief.eu" in url:
                usuarios.append(d['source']['title'])
            else:
                usuarios.append(NewsFeed['feed']['title'])
            if "newsbrief.eu" in url:
                textos.append(d['title'])
            else:
                textos.append(d['summary'])
            if "arxiv.org" in url:
                datas.append(NewsFeed['feed']['updated'])
            else:
                datas.append(d['published'])
    except:
        print("Erro em ", url)
    index = [hash(s) for s in textos]
    df = pd.DataFrame({'titulo': titulos,
                       'usuario': usuarios,
                       'data': datas,
                       'texto': textos,
                       'link': links}, index=index)
    df.texto = df.texto.apply(strip_html_tags)
    if NITTER_URL in url:
        df.usuario = df.usuario.apply(lambda x: x[1:])
    return(df)


def parse_listas(lista_usuarios_nitter, lista_urls_rss):
    nitter_url = NITTER_URL
    df = pd.DataFrame({'titulo': [],
                       'usuario': [],
                       'data': [],
                       'texto': [],
                       'link': []})
    for user in lista_usuarios_nitter:
        df_aux = retorna_noticias(nitter_url+user+"/rss")
        df = pd.concat([df, df_aux])
        df = df.drop_duplicates()
        time.sleep(5)
    for url in lista_urls_rss:
        df_aux = retorna_noticias(url)
        df = pd.concat([df, df_aux])
        df = df.drop_duplicates()
    return(df)


def pacote_noticias():
    lista_usuarios_pt = []
    lista_rss_pt = ["https://news.google.com/rss/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNREUxWm5JU0JYQjBMVUpTS0FBUAE?hl=pt-BR&gl=BR&ceid=BR%3Apt-419",
                    "https://news.google.com/rss/topics/CAAqLAgKIiZDQkFTRmdvSkwyMHZNR1ptZHpWbUVnVndkQzFDVWhvQ1FsSW9BQVAB?hl=pt-BR&gl=BR&ceid=BR%3Apt-419",
                    "https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFp1ZEdvU0JYQjBMVUpTR2dKQ1VpZ0FQAQ?hl=pt-BR&gl=BR&ceid=BR%3Apt-419",
                    "https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx1YlY4U0JYQjBMVUpTR2dKQ1VpZ0FQAQ?hl=pt-BR&gl=BR&ceid=BR%3Apt-419",
                    "https://news.google.com/rss/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx6TVdZU0JYQjBMVUpTR2dKQ1VpZ0FQAQ?hl=pt-BR&gl=BR&ceid=BR%3Apt-419",
                    "https://news.google.com/rss/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNR3QwTlRFU0JYQjBMVUpTS0FBUAE?hl=pt-BR&gl=BR&ceid=BR%3Apt-419",
                    "https://emm.newsbrief.eu/rss/rss?type=rtn&language=pt&duplicates=false"]
    lista_usuarios_en = []
    lista_rss_en = ["https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en",
                    "https://emm.newsbrief.eu/rss/rss?type=rtn&language=en&duplicates=false"]
    lista_usuarios_es = []
    lista_rss_es = ["https://emm.newsbrief.eu/rss/rss?type=rtn&language=es&duplicates=false",
                    "https://news.google.com/rss/topics/CAAqLAgKIiZDQkFTRmdvSUwyMHZNRGx1YlY4U0JtVnpMVFF4T1JvQ1ZWTW9BQVAB?hl=es-419&gl=US&ceid=US%3Aes-419"]
    lista_usuarios_it = []
    lista_rss_it = ["https://emm.newsbrief.eu/rss/rss?type=rtn&language=it&duplicates=false",
                    "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtbDBHZ0pKVkNnQVAB?hl=it&gl=IT&ceid=IT%3Ait"]
    lista_usuarios_fr = []
    lista_rss_fr = ["https://emm.newsbrief.eu/rss/rss?type=rtn&language=fr&duplicates=false",
                    "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtWnlHZ0pHVWlnQVAB?hl=fr&gl=FR&ceid=FR%3Afr"]
    lista_usuarios_de = []
    lista_rss_de = ["https://emm.newsbrief.eu/rss/rss?type=rtn&language=de&duplicates=false",
                    "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtUmxHZ0pFUlNnQVAB?hl=de&gl=DE&ceid=DE%3Ade"]
    lista_usuarios_ro = []
    lista_rss_ro = ["https://emm.newsbrief.eu/rss/rss?type=rtn&language=ro&duplicates=false",
                    "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FuSnZHZ0pTVHlnQVAB?hl=ro&gl=RO&ceid=RO%3Aro"]
    lista_usuarios_ca = []
    lista_rss_ca = [
        "https://emm.newsbrief.eu/rss/rss?type=rtn&language=ca&duplicates=false"]
    lista_usuarios_ds = ['AnalyticsVidhya', 'juliabloggers', 'Rbloggers', 'kdnuggets',
                         'TDataScience', 'TeachTheMachine', 'analyticbridge', 'paperswithcode',
                         'odsc', 'OpenAI', 'DeepMind', 'GoogleAI', 'Marktechpost']
    lista_rss_ds = ["http://export.arxiv.org/rss/cs.CL/recent",
                    "http://export.arxiv.org/rss/cs.CV/recent"]

    df = parse_listas(
        lista_usuarios_nitter=lista_usuarios_pt + lista_usuarios_en + lista_usuarios_es + lista_usuarios_it +
        lista_usuarios_fr + lista_usuarios_de + lista_usuarios_ro +
        lista_usuarios_ca + lista_usuarios_ds,
        lista_urls_rss=lista_rss_pt + lista_rss_en + lista_rss_es + lista_rss_es + lista_rss_it + lista_rss_fr + lista_rss_de + lista_rss_ro + lista_rss_ca + lista_rss_ds)
    return df
