import foodfuncs as ff
import utils as u


ifrec = input("Would you like to add another favorite recipe? Please type \'yes\' or \'no\':  ")
if ifrec.lower() == 'yes':
    u.new_recipe_prompt()
elif ifrec.lower() == 'no':
    max_oos = int(input("What is your maximum acceptable number of out-of-stock ingredients?  "))
    pick = u.pick_and_check(max_oos)
    if pick:
        print(f"\nRecipe: {pick['recipe']}\n")
        print(f"Difficulty: {pick['difficulty']}\n\nIngredients: ")
        for item in pick['ingredients']:
            print(item, " : ", pick['ingredients'][item])
        print(f"\nInstructions: {pick['instructions']}")
        print(f"Out of Stock: {', '.join(pick['out of stock'])}")

else:
    print("You did not enter \'y\' or \'n\'. Try again.")
    exit()
   
   
