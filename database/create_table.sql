-- ユーザー名「recipe_user」を作成する構文
CREATE USER recipe_user;

-- 権限にデータベース作成権限、ユーザー作成権限を加える（スーパーユーザーではない）
CREATE USER recipe_user WITH PASSWORD 'pass' CREATEDB LOGIN;

-- recipe db
CREATE DATABASE my_recipe_db;

-- recipe table
CREATE TABLE recipe (
    id SERIAL,
    menu varchar(50) NOT NULL,
    PRIMARY KEY (id)
) ;

-- ingredient table
CREATE TABLE ingredient (
    recipe_id Integer,
    name varchar(50) ,
    amount varchar(50) 
) ;
ALTER TABLE ingredient ALTER COLUMN amount TYPE varchar(50);

-- process table
CREATE TABLE process (
    recipe_id Integer,
    step_num Integer,
    step varchar(50)
) ;

-- レシピユーザーに権限を付与する
GRANT ALL ON my_recipe_db TO recipe_user
