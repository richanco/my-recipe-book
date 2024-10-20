import psycopg2

# recipeデータをデータベースに追加
def recipe_insert_db(recipe_data):
    # データベースに接続
    connection = psycopg2.connect("host=localhost user=recipe_user password=pass dbname=my_recipe_db")
    
    with connection:
        with connection.cursor() as cursor:
            # recipeテーブルにレシピ名を追加
            sql = "INSERT INTO recipe (menu) VALUES (%s) RETURNING id"
            cursor.execute(sql, (recipe_data['menu'],))
            # # 登録したレシピのidを取得
            recipe_id = cursor.fetchone()[0]
            
            # ingredientテーブルにレシピidと材料名、材料量を追加
            sql = "INSERT INTO ingredient (recipe_id , name, amount) VALUES (%s, %s, %s)"
            for ingredient in recipe_data['ingredients']:
              cursor.execute(sql, (recipe_id, ingredient['name'], ingredient['amount']))

            # processテーブルにレシピidと手順Noと手順内容を追加
            sql = "INSERT INTO process (recipe_id , step_num, step) VALUES (%s, %s, %s)"
            for process in recipe_data['processes']:
              cursor.execute(sql, (recipe_id, process['step_num'], process['step']))

        # コミットしてトランザクション実行
        connection.commit()