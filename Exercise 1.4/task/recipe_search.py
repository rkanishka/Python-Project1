import pickle

def display_recipe(recipe):
    print(f"Recipe: {recipe['name']}")
    print(f"Cooking Time: {recipe['cooking_time']} minutes")
    print(f"Ingredients: {', '.join(recipe['ingredients'])}")
    print(f"Difficulty: {recipe['difficulty']}")
    print()

def search_ingredient(data):
    print("Available ingredients:")
    for index, ingredient in enumerate(data["all_ingredients"], 1):
        print(f"{index}. {ingredient}")
    
    try:
        choice = int(input("Enter the number of the ingredient you want to search for: "))
        ingredient_searched = data["all_ingredients"][choice - 1]
    except (ValueError, IndexError):
        print("Invalid input. Please enter a valid number.")
        return
    
    print(f"\nRecipes containing {ingredient_searched}:")
    for recipe in data["recipes_list"]:
        if ingredient_searched in recipe["ingredients"]:
            display_recipe(recipe)

# Main code
filename = input("Enter the filename containing your recipe data: ")

try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    print(f"File '{filename}' not found.")
else:
    search_ingredient(data)