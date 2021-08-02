import random
import sqlite3
from sqlite3 import Error

def stocklist():
    """
    Input: a .txt of the food stock available
    Output: an iterable list of foods available 
    """
    file = open("stock.txt")
    foods = file.read().split("\n")
    file.close()

    return foods

def create_connection():
    """ create a database connection to the SQLite database recipes.db
    :return: Connection object or None
    """
    conn = None
    try:
        # waits for max of 30 seconds before closing the db to account for large recipes
        conn = sqlite3.connect("recipes.db")
        return conn
    except Error as e:
        print(e)

    return conn


def execute_no_params(sql_query):
    """execute a query without passed in parameters
    :param create_table_sql: a sql query 
    """
    try:
        conn = create_connection()
        c = conn.cursor()
        c.execute(sql_query)
        c.close()
        conn.close()
    except Error as e:
        pass

def execute_search(sql_query, params = 0):
    if params != 0:
        try:
            conn = create_connection()
            c = conn.cursor()
            result = c.execute(sql_query, params).fetchall()
            c.close()
            conn.close()
            return result
        except Error as e:
            pass
    else:
        try:
            conn = create_connection()
            c = conn.cursor()
            result = c.execute(sql_query).fetchall()
            c.close()
            conn.close()
            return result
        except Error as e:
            pass

def execute_insert(sql_query, params):
    if isinstance(params, list):
        try:
            conn = create_connection()
            c = conn.cursor()
            c.executemany(sql_query, params)
            conn.commit()
            c.close()
            conn.close()
        except Error as e: 
            pass
    else:
        try:
            conn = create_connection()
            c = conn.cursor()
            c.execute(sql_query, params)
            conn.commit()
            c.close()
            conn.close()
        except Error as e:
            pass

def is_tables():
    """Output: True if tables have been created, False if none."""
    query = """SELECT count(name) FROM recipes WHERE type='table' AND name='recipes'"""
    result = execute_no_params(query)
    if result:
        return True
    else:
        return False

def create_tables():
    # WORKS
    """ 
    Uses the execute_query function and the create_connection function
    to connect and create the initial tables. 
    """
    create_recipe_table = """CREATE TABLE recipes 
                                (recipe_id INTEGER PRIMARY KEY NOT NULL,
                                recipe_name TEXT, 
                                instructions_id INTEGER, 
                                difficulty_id INTEGER,
                                FOREIGN KEY (instructions_id) REFERENCES instructions(instructions_id) ON DELETE CASCADE,
                                FOREIGN KEY (difficulty_id) REFERENCES difficulty(difficulty_id) ON DELETE CASCADE
                                );"""
    create_instructions_table = """CREATE TABLE instructions
                                (instructions_id INTEGER PRIMARY KEY NOT NULL, 
                                instructions TEXT NOT NULL
                                );"""
    create_difficulty_table = """CREATE TABLE difficulty
                                (difficulty_id INTEGER PRIMARY KEY NOT NULL,
                                difficulty TEXT NOT NULL
                                );"""
    create_rec_ing_quan_table = """CREATE TABLE rec_ing_quan
                                    (recipe_id INTEGER, 
                                    ingredient_id INTEGER,
                                    quantity TEXT,
                                    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE,
                                    FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id) ON DELETE CASCADE
                                    );"""
    create_ingredients_table = """CREATE TABLE ingredients
                                    (ingredient_id INTEGER PRIMARY KEY NOT NULL,
                                    ingredient_name TEXT NOT NULL
                                    );"""
    create_table_queries = [create_difficulty_table, create_instructions_table, 
                            create_ingredients_table, create_recipe_table, 
                            create_rec_ing_quan_table]

    try:
        for query in create_table_queries:
            execute_no_params(query)
    except Error as e:
        print(e)

def populate_difficulty():
    "Executes the one-time population of the difficulty table."
    query = """INSERT INTO difficulty
                (difficulty_id, difficulty)
                VALUES 
                (?, ?)
            """
    params = [(1, "easy"), (2, "moderate"), (3, "hard")]

    execute_insert(query, params)

def rec_ing_instruc_new_ids():
    "returns a tuple of ints: new recipe id, new ingredient id, new instruction id"

    max_recipe_query = "SELECT MAX(recipe_id) FROM recipes;"
    max_recipe_id = execute_search(max_recipe_query)
    if max_recipe_id == [(None,)]:
        new_recipe_id = 0
    else:
        new_recipe_id = max_recipe_id[0][0] + 1

    max_ingredient_query = "SELECT MAX(ingredient_id) FROM ingredients;"
    max_ingredient_id = execute_search(max_ingredient_query)
    if max_ingredient_id == [(None,)]:
        new_ingredient_id = 0
    else: 
        new_ingredient_id = max_ingredient_id[0][0] + 1
    
    max__instruction_query = "SELECT MAX (instructions_id) FROM instructions;"
    max_instruction_id = execute_search(max__instruction_query)
    if max_instruction_id == [(None,)]:
        new_instruction_id = 0
    else: 
        new_instruction_id = max_instruction_id[0][0] + 1
    return new_recipe_id, new_ingredient_id, new_instruction_id


def insert_recipe(recipe, instructions, ingredients_quantities, difficulty):
    """
    param recipe: string name
    param instructions: string instructions
    param ingredients_quantities: dictionary of strings ingredient : quantity 
    param difficulty: int 1-3

    """
    recipe_query = """SELECT recipe_id FROM recipes
                        WHERE recipe_name = ?;"""
    recipe_id = execute_search(recipe_query, (recipe,))
    if recipe_id == [] or recipe_id == None:
        new_ids = rec_ing_instruc_new_ids()
        rec_id = new_ids[0]
        ing_id = new_ids[1]
        instruc_id = new_ids[2]
        rec_ing_quan_list = []
        ingredient_list = []
        ingredient_search = """SELECT ingredient_id FROM ingredients
                                WHERE ingredient_name = ?;"""

        for item in ingredients_quantities:
            try:
                ingredient_id = execute_search(ingredient_search, (item,))[0][0]
                rec_ing_quan_list.append((rec_id, ingredient_id, ingredients_quantities[item]))
            except:
                rec_ing_quan_list.append((rec_id, ing_id, ingredients_quantities[item]))
                ingredient_list.append((ing_id, item))
                ing_id += 1
            # populates properly
        instructions_data = (instruc_id, instructions)
        recipes_data = (rec_id, recipe, instruc_id, difficulty)
        instructions_query = """INSERT INTO instructions
                                (instructions_id, instructions)
                                VALUES 
                                (?, ?);"""
        ingredients_query = """INSERT INTO ingredients
                            (ingredient_id, ingredient_name)
                            VALUES 
                            (?, ?);"""
        recipes_query = """INSERT INTO recipes
                        (recipe_id, recipe_name, instructions_id, difficulty_id)
                        VALUES 
                        (?, ?, ?, ?);"""
        rec_ing_quan_query = """INSERT INTO rec_ing_quan
                            (recipe_id, ingredient_id, quantity)
                            VALUES
                            (?, ?, ?);"""
        execute_insert(instructions_query, instructions_data)
        execute_insert(ingredients_query, ingredient_list)
        execute_insert(recipes_query, recipes_data)
        execute_insert(rec_ing_quan_query, rec_ing_quan_list)
        print("the inserts were successful")
    else:
        print(f"This recipe already exists at id {recipe_id}.")

def pickrecipe():
    """
    Input: none
    Finds the highest recipe id number, and randint picks within the range 1 - max 
    Output: A dictionary as follows: 
    recipe: "", ingredients: {x: amnt,}, instructions: "", difficulty: ""
    OR False if no recipes to choose from
    """
    ids = rec_ing_instruc_new_ids()
    greatest_recipe = ids[0]
    if greatest_recipe > 0:
        greatest_recipe = greatest_recipe -1
    else:
        # no recipes to choose from
        return False
    try:
        full_recipe = {}
        pick = (random.randint(0, greatest_recipe),)

        recipe_query = """SELECT 
                            recipe_id, recipe_name, instructions_id, difficulty_id 
                        FROM recipes 
                        WHERE recipe_id = ?;"""
        recipe_row = execute_search(recipe_query, pick)
        full_recipe["recipe"] = recipe_row[0][1]

        rec_ing_quan_query = """SELECT ingredient_id, quantity 
                                FROM rec_ing_quan 
                                WHERE recipe_id = ?;"""
        ingredients_rows = execute_search(rec_ing_quan_query, pick)
        ing_dict = {}
        for item in ingredients_rows:
            ing_query = """SELECT ingredient_name
                            FROM ingredients
                            WHERE ingredient_id = ?;"""
            param = (item[0],)
            ing = execute_search(ing_query, param)[0][0]
            ing_dict[ing] = item[1]

        full_recipe["ingredients"] = ing_dict

        instruct_query = """SELECT instructions
                            FROM instructions
                            WHERE instructions_id = ?;"""
        param = (recipe_row[0][2],)
        instructions = execute_search(instruct_query, param)[0][0]
        full_recipe["instructions"] = instructions

        difficulty_query = """SELECT difficulty
                            FROM difficulty
                            WHERE difficulty_id = ?;"""
        param = (recipe_row[0][3],)
        difficulty = execute_search(difficulty_query, param)[0][0]
        full_recipe["difficulty"] = difficulty

        return full_recipe
    except sqlite3.Error as error:
        print("Error: cannot connect or find the recipe.", error)
   

def not_in_stock(full_recipe):
    """param full_recipe: dictionary of full recipe (result of the pick_recipe func)
        output: a List of items not currently in stock"""
    rec = []
    for item in full_recipe["ingredients"]:
        rec.append(item)

    stock = stocklist()

    stock = np.array(stock)
    rec = np.array(rec)
    
    return np.setdiff1d(rec, stock).tolist()