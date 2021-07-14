from foodfuncs import *
import sqlite3


ifrec = input("Would you like to add another favorite recipe? Please type \'y\' or \'n\':  ")
if ifrec == 'y':
    recname = input("Please enter the name of your recipe:  ")
    instruct = input("Please type the instructions for your recipe:  ")
    ingdict = {}
    ingr = ''
    while ingr != 'x':
        ingr = input("Enter the ingredient name. If there are no more ingredients, enter 'x' :  ") 
        amt = input("Enter the amount of the ingredient as used in your recipe:  ")
        if ingr != 'x' and ingr != 'X':
            ingdict[ingr.lower()] = amt.lower()
    print(f"Are these ingredients and amounts correct for your {recname} recipe?")
    for x in ingdict:
        print(x, ":", ingdict[x])
    add_new_recipe(recname, instruct, ingdict)
elif ifrec == 'n':
    pick = input("Would you like a random recipe?")
else:
    print("You did not enter \'y\' or \'n\'. Try again.")
#  this should be a while loop instead

   
   

