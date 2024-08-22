recipes_list = []
ingredients_list = []

def take_recipe():
    name = input("Enter the name of a recipe: ")
    cooking_time = int(input("Enter cooking time in minutes: "))
    ingredients = input("Enter the ingredients, separated by comma: ").split(',')
 

    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients,
    }
    return recipe

n = int(input("How many recipes would you like to enter? "))

for i in range(n):
    print(f"\nRecipe {i+1}")
    recipe = take_recipe()
    
    for ingredient in recipe['ingredients']: 
        if ingredient not in ingredients_list: 
            ingredients_list.append(ingredient) 
    recipes_list.append(recipe)

for recipe in recipes_list:
    cooking_time = recipe['cooking_time']
    num_ingredients = len(recipe['ingredients'])
    
    if cooking_time < 10 and num_ingredients < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        difficulty = "Medium"          
    elif cooking_time >= 10 and num_ingredients < 4:
        difficulty = "Intermediate"
    elif cooking_time >= 10 and num_ingredients >= 4:
        difficulty = "Hard"
    
    recipe['difficulty'] = difficulty

for recipe in recipes_list:
    print(f"\nRecipe: {recipe['name']}")
    print(f"Cooking Time: {recipe['cooking_time']} minutes")
    print(f"Ingredients: {', '.join(recipe['ingredients'])}")
    print(f"Difficulty: {recipe['difficulty']}")   

print("\nAll Ingredients:")
print(', '.join(ingredients_list))