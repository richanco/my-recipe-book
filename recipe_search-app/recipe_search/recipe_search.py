import psycopg2
import os

#  概要　　材料名からレシピデータを検索する
#  引数　　材料名　複数の引数をタプルで受けとる
#  戻り値
def recipe_search(*ingredient_name_args):
    # データベースに接続
    connection = psycopg2.connect(os.getenv("DB_PARAM"))
    
    with connection:
        with connection.cursor() as cursor:
            # 入力された材料名からレシピidとレシピ名を取得する
            sql = """SELECT 
                        recipe.id, 
                        menu 
                    FROM recipe
                    INNER JOIN (
                        SELECT 
                            id, 
                            COUNT(*) as cnt
                        FROM recipe
                        INNER JOIN ingredient ON recipe.id = ingredient.recipe_id
                        WHERE name ~ %s
                        GROUP BY id
                    ) ingredient_count 
                    ON recipe.id = ingredient_count.id
                    WHERE ingredient_count.cnt >= %s"""
            
            # 材料名を正規表現で検索
            search_ingredient = '|'.join('(.*'+ ingredient_name + '.*)' for ingredient_name in ingredient_name_args)
            # 実行処理
            cursor.execute(sql, (search_ingredient, len(ingredient_name_args)))
            
            # 取得したレシピをリストに一時退避
            recipe_list = []
            for recipe in cursor:
                recipe_list.append(recipe)

            recipe_data_list = []
            for recipe in recipe_list:
                # レシピID取得
                recipe_id   = recipe[0]
                # レシピ名取得
                recipe_menu = recipe[1]

                # 材料の抽出
                ingredient_list = []
                sql = """SELECT name, amount 
                       FROM ingredient
                       WHERE recipe_id = %s"""
                # 実行処理
                cursor.execute(sql, (recipe_id,))
                for ingredient in cursor:
                    dict_ingredient = {'name': ingredient[0], 'amount': ingredient[1]}
                    ingredient_list.append(dict_ingredient) 

                # 手順を抽出
                proc_list = []
                sql = """SELECT step_num, step 
                       FROM process
                       WHERE recipe_id = %s"""
                # 実行処理
                cursor.execute(sql, (recipe_id,))
                for process in cursor:
                    dict_process = {'step_num': process[0], 'step': process[1]}
                    proc_list.append(dict_process) 


                # 辞書データに変換                
                recipe_data = {
                    'menu': recipe_menu,
                    'ingredients': ingredient_list,
                    'processes' : proc_list
                }
                recipe_data_list.append(recipe_data)
            return recipe_data_list