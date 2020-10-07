import requests
import json
from bs4 import BeautifulSoup
import time

class WhatToEat():
    def __init__(self):
        super().__init__()
        self.baseURL = 'https://www.10000recipe.com/recipe/list.html?order=reco&page='
        self.result = {}
    
    # 페이지별 리스트
    def crawlList(self, PAGE):
        res = requests.get(f'{self.baseURL}{PAGE}')
        soup = BeautifulSoup(res.text, 'html.parser')
        id = [i['href'].split('/recipe/')[1] for i in soup.select('ul.common_sp_list_ul li.common_sp_list_li div.common_sp_thumb a.common_sp_link')]
        title = [j.text for j in soup.select('ul.common_sp_list_ul li.common_sp_list_li div.common_sp_caption .common_sp_caption_tit')]
        author = [k.text.replace('\n','') for k in soup.select('ul.common_sp_list_ul li.common_sp_list_li div.common_sp_caption .common_sp_caption_rv_name')]

        for i, j, k in zip(id, title, author):
            self.result[i] = {
                'title' : j,
                'author' : k,
                'link' : f'https://www.10000recipe.com/recipe/{i}'
            }
               
        
    def mp(self):
        print('')
        
    def insert2DB(self):
        print('')
        
        
        
if __name__ == "__main__":
    wte = WhatToEat()
    PAGE = 1
    
    while(True):
        try:
            print(f'{PAGE} PAGE CRAWLING ...')
            wte.crawlList(PAGE)
            PAGE += 1
            time.sleep(1)
        except:
            break
    
    with open('page.json', 'w', encoding='utf-8') as f:
        json.dump(wte.result, f, ensure_ascii=False)
        
    