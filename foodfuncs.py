import random
import sqlite3
from sqlite3 import Error
# holds ordered list of all recipe names, checked by is_recipe_duplicate
reclist = []
# holds ordered list of all ingredients, checked by is_ingredient_duplicate 
inglist = []

def reclist_add(id, name):
    """input: int id, string name
        output: writes id and recipe to the reclist file for checking to reduce query volume"""
    # keeps track of current recipes in db to reduce query volume, used in insert_recipe
    file = open("reclist.txt", "a")
    towrite = "\n" + str(id) + ", " + name 
    file.write(towrite)
    file.close()

def inglist_add(ingredients):
    # WORKS
    """input: list of tuples (id, name)
    output: writes ids and ingredients to the inglist file for checking and query volume reduction"""
    file = open("inglist.txt", "a")
    for ing in ingredients:
        towrite = "\n" + str(ing[0]) + ", " + ing[1]
        file.write(towrite)
    file.close()

def stocklist(pantryfile):
    """
    Input: a .txt of the food stock available
    Output: an iterable list of foods available 
    """
    file = open(pantryfile)
    foods = file.read().split("\n")
    file.close()

    return foods

def pickrecipe ():
    """
    Input: none
    Finds the highest recipe id number, and randint picks within the range 1 - max 
    Output: A dictionary as follows: Recipe: "", Instructions: "", Ingredients: {x: amnt, etc}
    """
    idtup = greatest_ids()
    rec_id = int(idtup[0])

    try:
        conn = create_connection("recipes.db")
        cur = conn.cursor()
        pick = random.randint(1, rec_id)

        recipe_pick = (cur.execute("SELECT recipe_name FROM recipes WHERE id = ?", (pick,),).fetchall())[0][0]
        instructions_pick = (cur.execute("SELECT instructions FROM recipes WHERE id = ?", (pick,),).fetchall())[0][0]
        ingredient_id_quantity = cur.execute("SELECT * FROM ingrecipe WHERE recipe_id = 4").fetchall()
        
        finaldict = {'name' : recipe_pick,
                    'instructions' : instructions_pick,
                    'ingredients' : {}
        }
        for x in ingredient_id_quantity:
            ingredient_name = cur.execute("SELECT ingredient_name FROM ingredients WHERE id = ?",(x[1],),).fetchall()[0][0]
            finaldict['ingredients'][ingredient_name] = x[2]
        print(finaldict)
        # use recipe id to get a list of ingredient ids from ingrecipe
        # then use the ing ids to get ingredient names in loop with ing quantity
    except sqlite3.Error as error:
        print("Error: cannot connect or find the ingredient.", error)
    finally:
        if conn:
            conn.close()


    # iter = list(recipes.items())
    # pick = random.choice(iter)

    # while all(x in foodavail for x in pick[1])is not True:
    #     pick = random.choice(iter)

    # return pick 

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        # waits for max of 30 seconds before closing the db to account for large recipes
        conn = sqlite3.connect(db_file, timeout=30.0)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        c.close()
    except Error as e:
        print(e)


def full_create_tables():
    """ 
    Uses the create_table function and the create_connection function
    to connect and create the initial tables. 
    """
    database = r"recipes.db"

    sql_create_recipe_table = """CREATE TABLE recipes 
                                (id INTEGER PRIMARY KEY NOT NULL, 
                                recipe_name TEXT NOT NULL, 
                                instructions TEXT);
                                """
    sql_create_ingredients_table = """ CREATE TABLE ingredients
                                    (id INTEGER PRIMARY KEY NOT NULL, 
                                    ingredient_name TEXT NOT NULL
                                    );"""

    sql_create_ingrecipe_table = """CREATE TABLE ingrecipe
                                (recipe_id INTEGER NOT NULL,
                                ingredient_id INTEGER NOT NULL, 
                                quantity TEXT,
                                FOREIGN KEY (recipe_id) REFERENCES recipes (id) ON DELETE CASCADE,
                                FOREIGN KEY (ingredient_id) REFERENCES ingredients (id) ON DELETE CASCADE
                                );"""
 # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create recipe table
        create_table(conn, sql_create_recipe_table)

        # create ingredients table
        create_table(conn, sql_create_ingredients_table)

        # create ingrecipe table
        create_table(conn, sql_create_ingrecipe_table)

        conn.close()
    else:
        print("Error! cannot create the database connection.")

def find_ingredient_id(name):
   # WORKS
    """input: ingredient name
        output: integer id of the ingredient in ingredient table, if doesn't
        exist, False
    """
    file = open("inglist.txt")
    ingredients = file.read().split("\n")
    file.close()
    for item in ingredients: 
        n = item.split(", ")
        if n[1] == name:
            return int(n[0])
    return False
    

    # try:
    #     conn = create_connection("recipes.db")
    #     cur = conn.cursor()
    #     # Look up the id of a dup ingredient by the ingredient name
    #     id_ing = cur.execute("SELECT id FROM ingredients WHERE ingredient_name = ?", (name,),).fetchall()
    #     cur.close()
    #     return id_ing[0]
    # except sqlite3.Error as error:
    #     print("Error: cannot connect or find the ingredient.", error)
    # finally:
    #     if conn:
    #         conn.close()
    #         print("the connection is closed.")

def insert_recipe(recipe):
    """
    input: a tuple (id, recipe_name, instructions)
    output: populates the recipes db with 1 recipe
    """
    
    try:
        conn = create_connection("recipes.db")
        cur = conn.cursor()
        # Inserts one row of recipe by command, then 
        recipe_query = """ INSERT INTO recipes 
                            (id, recipe_name, instructions)
                            VALUES 
                            (?, ?, ?);"""
        
        cur.execute(recipe_query, recipe)
        conn.commit() 
        print(f"{recipe[1]} recipe inserted successfully")
        cur.close()
        if conn:
            conn.close()
            print("the connection is closed.")
            # adds the new recipe to the reclist 
            reclist_add(recipe[0], recipe[1])
    except sqlite3.Error as error:
        print("Failed to connect and insert data", error)


def insert_ingredients(ingredientList):
    """
    input: a list of tuples [(id, ingredient_name), (), ()]
    output: populates the ingredients db with ingredients
    """
    try:
        conn = create_connection("recipes.db")
        cur = conn.cursor()

        query = """ INSERT INTO ingredients 
                            (id, ingredient_name)
                            VALUES 
                            (?, ?);"""
        # repeatedly executes the query until the list has ended and id/ing pairs are inserted
        cur.executemany(query, ingredientList)
        conn.commit() 
        print(f"{cur.rowcount} ingredients inserted successfully")
        cur.close()
        if conn:
            conn.close()
            print("the connection is closed.")
            # adds the new ingredient to the inglist
            inglist_add(ingredientList)
    except sqlite3.Error as error:
        print("Failed to connect and insert data", error)


def insert_ingrecipe(ingrecipeList):
    """
    input: a list of tuples (recipe_id, ingredient_id, quantity)
    output: populates the recipes db with recipe
    """
    try:
        conn = create_connection("recipes.db")
        cur = conn.cursor()

        ingrecipe_query = """ INSERT INTO ingrecipe 
                            (recipe_id, ingredient_id, quantity)
                            VALUES 
                            (?, ?, ?);"""
        # repeatedly inserts the query until the list of (recid, ingid, quant) is exhausted
        cur.executemany(ingrecipe_query, ingrecipeList)
        conn.commit() 
        print(f"{cur.rowcount} ingrecipes inserted successfully")
        cur.close()
        if conn:
            conn.close()
            print("the connection is closed.")
    except sqlite3.Error as error:
        print("Failed to connect and insert data", error)


def is_recipe_duplicate(name):
     # WORKS
    """input: name of recipe that user is trying to insert
        output: true if duplicate, false if not
    """
    # reads reclist, loops through entries and separates out recipe names to compare to name
    file = open("reclist.txt")
    recipes = file.read().split("\n")
    file.close()
    for item in recipes:
        n = item.split(", ")
        if n[1] == name:
            return True
    return False
    # try:
    #     conn = create_connection("recipes.db")
    #     cur = conn.cursor()
    #     dup = cur.execute("SELECT id FROM recipes WHERE recipe_name = ?", (name,),).fetchall()
    #     if dup:
    #         return True
    #     else: 
    #         return False
    # except sqlite3.Error as error:
    #     print("There was an error: ", error)
    # finally:
    #     if conn:
    #         conn.close()
    #         print("the connection is closed.")

def is_ingredient_duplicate(name):
    # WORKS
    """input: name of ingredient that user is trying to insert
        output: true if duplicate, false if not
    """
    # reads inglist, loops through entries and separates out ingredient names to compare to name
    file = open("inglist.txt")
    ingredients = file.read().split("\n")
    file.close()
    for item in ingredients: 
        n = item.split(", ")
        if n[1] == name:
            return True
    return False
    # try:
    #     conn = create_connection("recipes.db")
    #     cur = conn.cursor()
    #     dup = cur.execute("SELECT id FROM ingredients WHERE ingredient_name = ?", (name,),).fetchall()
    #     if dup:
    #         return True
    #     else:
    #         return False
    # except sqlite3.Error as error:
    #     print("There was an error: ", error)
    # finally:
    #     if conn:
    #         conn.close()
    #         print("the connection is closed.")

def greatest_ids():
    # DOESN'T WORK
    """ output: tuple of recipe id and ingredient id integers
    """
    reclist = open("reclist.txt")
    inglist = open("inglist.txt")
    rec = reclist.read().split("\n")
    ing = inglist.read().split("\n")
    if rec != [] and ing != []:
        # loop through the list, split each item and return it to the spot 
        for index, i in enumerate(ing):
            i = tuple(i.split(", "))
            ing[index] = i
        for ind, r in enumerate(rec):
            r = tuple(r.split(", "))
            rec[ind] = i 
        return int(rec.pop()[0]), int(ing.pop()[0])
    else: 
        return 0, 0
    # try:
    #     conn = create_connection("recipes.db")
    #     cur = conn.cursor()
    #     rec = cur.execute("SELECT MAX(id) FROM recipes").fetchall()
    #     ing = cur.execute("SELECT MAX(id) FROM ingredients").fetchall()
    #     if type(rec[0][0]) == int and type(ing[0][0]) == int:
    #         recipe = rec[0][0]
    #         ingredient = ing[0][0]
    #     else:
    #         recipe = 0
    #         ingredient = 0
    #     cur.close()
    #     if conn: 
    #         conn.close()
    #     return recipe, ingredient
    # except sqlite3.Error as error:
    #     print(f"Could not connect and find max values: {error}")


def add_new_recipe(recipe_name, instructions, ingredients):
    """
    input: string recipe_name, string instructions, dictionary of 
    ingredients with associated quantities
    Checks for duplicate recipe and ingredients with is_duplicate_?
    assigns an id to recipe and each ingredient that is at least 
    one more than the greatest id using greatest_id
    Adds respective data points to the db
    """
    inglist = []
    ingreclist = []
    # finds the last id or 0 if table is empty, then add 1 to provide the next id
    if greatest_ids():
        start_ids = greatest_ids()
        rec = start_ids[0] + 1
        ing = start_ids[1] + 1
    else:
        print("Something went wrong with greatest ids.")
        return "something went wrong with greatest ids."
    # Checks if the recipe is already here before inserting id, name and instructions
    if is_recipe_duplicate(recipe_name) == False: 
        insrec = (rec, recipe_name, instructions)
        insert_recipe(insrec)
    # If it is a duplicate, the process doesn't continue and it prints a message
    elif is_recipe_duplicate == True: 
        print("This recipe already exists")
        return "This recipe already exists."
    # Checks through the ingredient/quantity dictionary for duplicates; if none, it adds
    # the new ingredient id and the name to the ing list of tuples for population
    for i in ingredients: 
        if is_ingredient_duplicate(i) == False:
            inglist.append((ing, i))
            ingreclist.append((rec, ing, ingredients[i]))
            ing += 1
        else:
            # finds the duplicate ingredient id, forgoes adding to ingredients_list(already there)
            # populate a list of tuples with recipe id, the duplicate ing id,
            # and quantity to pass into the ingrecipe table
            x = find_ingredient_id(i)
            ingreclist.append((rec, x, ingredients[i]))
    insert_ingredients(inglist)
    insert_ingrecipe(ingreclist)
   