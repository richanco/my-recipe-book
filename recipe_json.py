import requests
from bs4 import BeautifulSoup

#　取得したデータをJsonデータに変換する
def recipe_to_json(cook_url):
  # 抽出したレシピURLから、レシピ名・材料・手順を抽出する
  # スクレイピング対象をURLにリストを送りHTMLを取得する
  res = requests.get(cook_url)
  # レスポンスのHTMLからBeautifulSoupのオブジェクトを作成する
  soup = BeautifulSoup(res.text, 'html.parser')
  
  # レシピ名取得
  menu = soup.find('h1').getText().strip()

  # 材料の抽出
  ingredient_list = []
  ingredients_list = soup.select('#ingredients > div.ingredient-list > ol > li')
  for ingredient in ingredients_list:
      # 材料名を取得
      ingredient_name = ingredient.find('span').getText()
      # 材料の量を取得
      ingredient_amount = ingredient.find('bdi').getText()
      
      dict_ingredient = {'name': ingredient_name, 'amount': ingredient_amount}
      ingredient_list.append(dict_ingredient)

  # 手順を抽出
  proc_list = []
  process_tag_list = soup.select('#steps > ol > li ')
  step_num = 1
  for process in process_tag_list:
      # 手順を取得
      step = process.find('p').getText()
      dict_process = {'step_num': step_num, 'step':step}
      proc_list.append(dict_process)
      step_num = step_num + 1

  # 辞書データに変換
  recipe_data = {
    'menu': menu,
    'ingredients': ingredient_list,
    'processes' : proc_list
  }
  return recipe_data
