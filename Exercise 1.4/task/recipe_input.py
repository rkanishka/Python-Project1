import pickle

def take_recipe():
    name = input("Enter the recipe name: ")
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    ingredients = input("Enter the ingredients, separated by a comma: ").split(",")
    ingredients = [ingredient.strip() for ingredient in ingredients]
    
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
    }
    
    recipe["difficulty"] = calc_difficulty(recipe)
    return recipe


def calc_difficulty(recipe):
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        return "Easy"
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        return "Medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        return "Intermediate"
    else:
        return "Hard"


# Main code
filename = input("Enter the filename to store/load recipes: ")

try:
    with open(filename, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    data = {"recipes_list": [], "all_ingredients": []}
except:
    print("Unexpected error. Creating new data structure.")
    data = {"recipes_list": [], "all_ingredients": []}
else:
    file.close()
finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]

n = int(input("How many recipes would you like to enter? "))

for i in range(n):
    recipe = take_recipe()
    recipes_list.append(recipe)
    for ingredient in recipe["ingredients"]:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}

with open(filename, 'wb') as file:
    pickle.dump(data, file)

print(f"Recipe data has been saved to {filename}")