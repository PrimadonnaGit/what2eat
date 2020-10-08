import requests
import json
import time
import pymysql

from bs4 import BeautifulSoup

# 49.247.134.77 sparker kr01!

class WhatToEat():
  def __init__(self):
    super().__init__()
    self.baseURL = 'https://www.10000recipe.com/recipe/list.html?order=reco&page='
    self.result = {}
    self.initDB()

  def initDB(self):
    self.conn = pymysql.connect(host='49.247.134.77',
                      port=3306,
                      user='sparker',
                      passwd='tlchd50wh!',
                      db='what2eat')
  

  def insertDB(self, result):
    cur = self.conn.cursor()

    # platform, key, title, author, link
    q = f"INSERT INTO recipe_list (platform, lkey, title, author, link) VALUES {result} ON DUPLICATE KEY UPDATE lkey = VALUES(lkey)"
    cur.execute(q)
    self.conn.commit()
    cur.close()

  def insertDBdetail(self, result):
    cur = self.conn.cursor()

    # key, ingredients, summary1, summary2, summary3
    q = f"INSERT INTO recipe_detail (lkey, ingredients, summary1, summary2, summary3) VALUES {result} ON DUPLICATE KEY UPDATE lkey = VALUES(lkey)"
    cur.execute(q)
    self.conn.commit()
    cur.close()

  def selectDB(self):
    cur = self.conn.cursor()

    q = f"select lkey from recipe_list"
    cur.execute(q)
    recipes = [r[0] for r in cur.fetchall()]
    cur.close()

    return recipes
    
  
  # 페이지별 리스트
  def crawlList(self, PAGE):
    res = requests.get(f'{self.baseURL}{PAGE}')
    soup = BeautifulSoup(res.text, 'html.parser')
    id = [i['href'].split('/recipe/')[1] for i in soup.select('ul.common_sp_list_ul li.common_sp_list_li div.common_sp_thumb a.common_sp_link')]
    title = [j.text for j in soup.select('ul.common_sp_list_ul li.common_sp_list_li div.common_sp_caption .common_sp_caption_tit')]
    author = [k.text.replace('\n','') for k in soup.select('ul.common_sp_list_ul li.common_sp_list_li div.common_sp_caption .common_sp_caption_rv_name')]

    for lkey, title, author in zip(id, title, author):
      title = title.replace('"','').strip()
      author = author.replace('"','').strip()
      result = f'("만개의레시피","{lkey}","{title}","{author}","https://www.10000recipe.com/recipe/{lkey}")'
      self.insertDB(result)

  def crawlDetail(self, lkey):
    res = requests.get(f'https://www.10000recipe.com/recipe/{lkey}')
    soup = BeautifulSoup(res.text, 'html.parser')
    ingredients = [i.text.split('                                                        ')[0].strip() for i in soup.select('#divConfirmedMaterialArea > ul li')]
    ingredients_val = [j.text for j in soup.select('#divConfirmedMaterialArea > ul li > span')]
    summary1 = soup.select_one('#contents_area > div.view2_summary > div.view2_summary_info > .view2_summary_info1')
    summary2 = soup.select_one('#contents_area > div.view2_summary > div.view2_summary_info > .view2_summary_info2')
    summary3 = soup.select_one('#contents_area > div.view2_summary > div.view2_summary_info > .view2_summary_info3')

    if not summary1: summary1 = ''
    else: summary1 = summary1.text
    if not summary2: summary2 = ''
    else: summary2 = summary2.text
    if not summary3: summary3 = ''
    else: summary3 = summary3.text

    ingredient = '|'.join([f'{i}-{j}' for i,j in zip(ingredients, ingredients_val)])
    result = f'("{lkey}", "{ingredient}", "{summary1}", "{summary2}", "{summary3}")'
    self.insertDBdetail(result)
      
        
if __name__ == "__main__":
  wte = WhatToEat()
  # PAGE = 1
  
  # while(True):
  #   try:
  #     print(f'{PAGE} PAGE CRAWLING ...')
  #     wte.crawlList(PAGE)
  #     PAGE += 1
  #     time.sleep(1)
  #   except Exception as e:
  #     print(e)
  #     break

  # wte.conn.close()

  # DETAIL

  recipes = wte.selectDB()

  for lkey in recipes:
    print(lkey)
    wte.crawlDetail(lkey)

    