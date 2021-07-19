from foodfuncs import *









# instructions = "Boil the pasta, strain out the water. Mix in butter, milk, and sauce packet over low heat."
# # ingredients is not populated - says unnique constrint failed for that table
# inglist = [(0, "mac", "1 box"), (0, "milk", "1/4 cup"), (0, "butter", "1 tbsp"), (0, "sauce packet", "1")]
# recipe = "mac n cheese"
# insert = (recipe, instructions)
# query = """INSERT INTO rec_ing_quan 
#         (recipe_id, ingredient, quantity)
#         VALUES 
#         (?, ?, ?);"""
# id = execute_query(query, inglist)

# ifrec = input("Would you like to add another favorite recipe? Please type \'y\' or \'n\':  ")
# if ifrec == 'y':
#     recname = input("Please enter the name of your recipe:  ")
#     instruct = input("Please type the instructions for your recipe:  ")
#     ingdict = {}
#     ingr = ''
#     while ingr != 'x':
#         ingr = input("Enter the ingredient name. If there are no more ingredients, enter 'x' :  ") 
#         amt = input("Enter the amount of the ingredient as used in your recipe:  ")
#         if ingr != 'x' and ingr != 'X':
#             ingdict[ingr.lower()] = amt.lower()
#     print(f"Are these ingredients and amounts correct for your {recname} recipe?")
#     for x in ingdict:
#         print(x, ":", ingdict[x])
#     add_new_recipe(recname, instruct, ingdict)
# elif ifrec == 'n':
#     pick = input("Would you like a random recipe?")
# else:
#     print("You did not enter \'y\' or \'n\'. Try again.")
# #  this should be a while loop instead

   
   
