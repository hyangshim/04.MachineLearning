import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import pandas as pd
def news():
    for page in range(1,3):
        url=f'https://kormedi.com/healthnews/page/{page}/'
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
        result = requests.get(url, headers=header)
        soup = BeautifulSoup(result.text, 'html.parser')
        h2s =soup.select('article')
        My_list =[]
        h2 =h2s[0]
        for h2 in h2s:
            title= h2.select_one('.title').get_text().strip()
            image =h2.select_one('a')['data-bg']
            link =h2.select_one('a')['href']
            My_list.append({'제목':title,'이미지':image,'링크':link})
    return My_list