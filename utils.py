from typing import Set
import foodfuncs as ff

def new_recipe_prompt():
    """Runs a script in which the user can enter a recipe and check if it is correct.
    If it is correct, the recipe is inserted into the database."""

    name = input("Please enter the name of your recipe:  ").lower()
    instruct = input("Please type the instructions for your recipe:  ")
    difficulty = int(input("Using numbers 1-3, how difficult is this recipe?  "))
    while difficulty < 1 or difficulty > 3:
        difficulty = int(input("The number you entered is incorrect. Please enter a number from 1 - 3.  "))
    ingdict = {}
    ingr = ''
    while ingr != 'x':
        ingr = input("Enter the ingredient name. If there are no more ingredients, enter 'x' :  ") 
        if ingr != 'x' and ingr != 'X':
            amt = input("Enter the amount of the ingredient as used in your recipe:  ")
            ingdict[ingr.lower()] = amt.lower()
        
    for x in ingdict:
        print(x, ":", ingdict[x])
    print(instruct)
    print(f"Difficulty: {difficulty}")
    feedback = input(f"Are these ingredients, amounts, and instructions correct for your {name} recipe? Please type \'yes\' or \'no\':  ")
    if feedback.lower() == 'no':
        print("Please start the program again and re-enter your recipe.")
        exit()
    elif ff.is_tables() == False:
        ff.create_tables()
        ff.populate_difficulty()
        ff.insert_recipe(name, instruct, ingdict, difficulty)
    else:
        ff.insert_recipe(name, instruct, ingdict, difficulty)
    
def pick_and_check(max_oos):
    """param max_oos: int acceptable number of out of stock ingredients
        returns recipe under required number of out of stock
        returns False if all recipes do not meet out of stock requirements
        returns None if no recipes in the database
        Recipe has added dictionary entry "Out of Stock" : list of ingredients """
    recipe = ff.pickrecipe()
    if recipe is not False:
        checked = set()
        oos_list = ff.not_in_stock(recipe)
        max_rec_id = ff.rec_ing_instruc_new_ids()[0] - 1
        while len(oos_list) > max_oos:
            checked.add(recipe["recipe"])
            if len(checked) == max_rec_id:
                return False
            else:
                recipe = ff.pickrecipe()
                oos_list = ff.not_in_stock(recipe)
        recipe["out of stock"] = oos_list
        return recipe
    else:
        return None
