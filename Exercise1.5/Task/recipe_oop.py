# recipe_oop.py

class Recipe:
    all_ingredients = set()  # Class variable to store all unique ingredients

    def __init__(self, name):
        self._name = name
        self._ingredients = []
        self._cooking_time = 0
        self._difficulty = None

    # Getter and setter for name
    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    # Getter and setter for cooking_time
    def get_cooking_time(self):
        return self._cooking_time

    def set_cooking_time(self, cooking_time):
        self._cooking_time = cooking_time
        self._difficulty = None  # Reset difficulty when cooking time changes

    # Method to add ingredients
    def add_ingredients(self, *ingredients):
        self._ingredients.extend(ingredients)
        self._difficulty = None  # Reset difficulty when ingredients change
        self.update_all_ingredients()

    # Getter for ingredients
    def get_ingredients(self):
        return self._ingredients

    # Method to calculate difficulty
    def calculate_difficulty(self):
        if self._cooking_time < 10 and len(self._ingredients) < 4:
            self._difficulty = "Easy"
        elif self._cooking_time < 10 and len(self._ingredients) >= 4:
            self._difficulty = "Medium"
        elif self._cooking_time >= 10 and len(self._ingredients) < 4:
            self._difficulty = "Intermediate"
        else:  # cooking_time >= 10 and len(ingredients) >= 4
            self._difficulty = "Hard"

    # Getter for difficulty
    def get_difficulty(self):
        if self._difficulty is None:
            self.calculate_difficulty()
        return self._difficulty

    # Method to search for an ingredient
    def search_ingredient(self, ingredient):
        return ingredient.lower() in (i.lower() for i in self._ingredients)

    # Method to update all_ingredients
    def update_all_ingredients(self):
        Recipe.all_ingredients.update(self._ingredients)

    # String representation of the recipe
    def __str__(self):
        return (f"Recipe: {self._name}\n"
                f"Cooking Time: {self._cooking_time} minutes\n"
                f"Ingredients: {', '.join(self._ingredients)}\n"
                f"Difficulty: {self.get_difficulty()}")

def recipe_search(data, search_term):
    print(f"\nRecipes containing {search_term}:")
    for recipe in data:
        if recipe.search_ingredient(search_term):
            print(recipe)

# Main code
if __name__ == "__main__":
    # Create Tea recipe
    tea = Recipe("Tea")
    tea.add_ingredients("Tea Leaves", "Sugar", "Water")
    tea.set_cooking_time(5)
    print(tea)

    # Create Coffee recipe
    coffee = Recipe("Coffee")
    coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
    coffee.set_cooking_time(5)
    print(coffee)

    # Create Cake recipe
    cake = Recipe("Cake")
    cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
    cake.set_cooking_time(50)
    print(cake)

    # Create Banana Smoothie recipe
    banana_smoothie = Recipe("Banana Smoothie")
    banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
    banana_smoothie.set_cooking_time(5)
    print(banana_smoothie)

    # Create recipes list
    recipes_list = [tea, coffee, cake, banana_smoothie]

    # Search for recipes containing specific ingredients
    recipe_search(recipes_list, "Water")
    recipe_search(recipes_list, "Sugar")
    recipe_search(recipes_list, "Bananas")

    print("\nAll ingredients used across recipes:", Recipe.all_ingredients)