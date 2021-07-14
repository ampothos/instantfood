# Plan

Local program for favorite recipes

### Functionality:

    -Easily insert recipe, ingredients, description and amounts
    - Load in a new text file of stock every time? or have one to modify?

# Log

## 7.13

Previous testing and deletions in the db were done improperly because of foreign key constraints, so full_create_tables was modified for foreign keys to cascade on deletion, and I recreated the whole db.

Still not working - thinks recipe ids start at 6 and there are still duplicates, even though the whole database was deleted. Recipes is not populating at all, ingrecipes populates completely with incorrect ids out of order, and ingredients populated only the first and third insertions (thighs and chili). It's because I din't update the text files.

The duplicate checking is flawed, otherwise this would have been caught. Look at that after populating properly.
File "C:\Users\Jrive\Desktop\alainna's projects\instantfood\main.py", line 19, in <module>
add_new_recipe(recname, instruct, ingdict)
File "C:\Users\Jrive\Desktop\alainna's projects\instantfood\foodfuncs.py", line 373, in add_new_recipe  
 if greatest_ids():
File "C:\Users\Jrive\Desktop\alainna's projects\instantfood\foodfuncs.py", line 339, in greatest_ids
return int(rec.pop()[0]), int(ing.pop()[0])
ValueError: invalid literal for int() with base 10: ''

Catch empty files to start the database in greatest_ids

## 7.12

Use two txt documents, reclist and inglist, to reduce query volumes and check for instances of recipes and ingredients. Each time an ingredient is inserted in the final add_recipe function, is_x_duplicate checks with each list before giving the go ahead. Once not duplicate, when the recipe is added, insert_rec/ing is called and rec/ing_add is called within insert.

- x is_duplicate checks lists, not queries
- x greatest_ids checks lists, not queries
- x insert_recipe and insert_ingredients + listadd func
- x find_ingredient_id replaced with doc search

## 6.18

Created functions to comprehensively add new recipes to the tables, manage connections and cursors, check for duplicates, and manage ids.
Function add_new_recipe uses create_connection, checks if recipe or ingredients exist with is_recipe_duplicate and is_ingredient_duplicate (may be ingredients shared between recipes, but always only 1 copy of the ingredient with its unique id), assigns ids by finding greatest with greatest_ids and assigning, incrementing by 1 for recipe and for each ingredient. Adds each data point and id to each respective column and table with insert_recipe, insert_ingredients, and insert_ingrecipe.

## 6.17

Created the tables within the database, and functions to create new tables and manage connections.

## 6.16

Created foodfuncs.py, which contains the functions stocklist(), a function that turns the text file of food stock into a list, and pickrecipe(), which chooses a random recipe from the database and ensures that all the ingredients are in stock.

Created the sqlite database where the recipes will be stored.

