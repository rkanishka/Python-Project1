from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("mysql+pymysql://cf-ipython:password@localhost/task_database")
Session = sessionmaker(bind=engine)
session = Session()

class Recipe(Base):
    __tablename__ = 'final_recipes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return f"<Recipe(id={self.id}, name='{self.name}', difficulty='{self.difficulty}')>"

    def __str__(self):
        return f"""
        Recipe: {self.name}
        ========================
        Ingredients: {self.ingredients}
        Cooking Time: {self.cooking_time} minutes
        Difficulty: {self.difficulty}
        """

    def calculate_difficulty(self):
        ingredients_list = self.return_ingredients_as_list()
        if self.cooking_time < 10 and len(ingredients_list) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(ingredients_list) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(ingredients_list) < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"

    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        return self.ingredients.split(', ')

Base.metadata.create_all(engine)

def create_recipe():
    name = input("Enter recipe name (max 50 characters): ")
    while len(name) > 50 or not name.replace(' ', '').isalnum():
        name = input("Invalid input. Please enter a valid recipe name (max 50 characters): ")

    ingredients = []
    num_ingredients = int(input("How many ingredients would you like to enter? "))
    for i in range(num_ingredients):
        ingredient = input(f"Enter ingredient {i+1}: ")
        ingredients.append(ingredient)
    
    ingredients_str = ', '.join(ingredients)

    cooking_time = input("Enter cooking time (in minutes): ")
    while not cooking_time.isnumeric():
        cooking_time = input("Invalid input. Please enter a valid cooking time (in minutes): ")
    cooking_time = int(cooking_time)

    recipe_entry = Recipe(
        name=name,
        ingredients=ingredients_str,
        cooking_time=cooking_time
    )
    recipe_entry.calculate_difficulty()

    session.add(recipe_entry)
    session.commit()
    print("Recipe added successfully!")

def view_all_recipes():
    recipes = session.query(Recipe).all()
    if not recipes:
        print("There are no recipes in the database.")
        return None
    
    for recipe in recipes:
        print(recipe)

def search_by_ingredients():
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database.")
        return None

    results = session.query(Recipe.ingredients).all()
    all_ingredients = []
    for result in results:
        ingredients = result[0].split(', ')
        for ingredient in ingredients:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)

    print("Available ingredients:")
    for i, ingredient in enumerate(all_ingredients, 1):
        print(f"{i}. {ingredient}")

    search_input = input("Enter the numbers of ingredients you want to search for (separated by spaces): ")
    search_numbers = search_input.split()
    
    try:
        search_numbers = [int(num) for num in search_numbers]
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return None

    if not all(1 <= num <= len(all_ingredients) for num in search_numbers):
        print("Invalid ingredient number(s) selected.")
        return None

    search_ingredients = [all_ingredients[num-1] for num in search_numbers]

    conditions = []
    for ingredient in search_ingredients:
        like_term = f"%{ingredient}%"
        conditions.append(Recipe.ingredients.like(like_term))

    matching_recipes = session.query(Recipe).filter(*conditions).all()

    if matching_recipes:
        print("Matching recipes:")
        for recipe in matching_recipes:
            print(recipe)
    else:
        print("No recipes found with the selected ingredients.")

def edit_recipe():
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database.")
        return None

    results = session.query(Recipe.id, Recipe.name).all()
    print("Available recipes:")
    for id, name in results:
        print(f"{id}. {name}")

    recipe_id = input("Enter the ID of the recipe you want to edit: ")
    if not recipe_id.isnumeric():
        print("Invalid input. Please enter a valid recipe ID.")
        return None

    recipe_to_edit = session.query(Recipe).filter_by(id=int(recipe_id)).first()
    if not recipe_to_edit:
        print("Recipe not found.")
        return None

    print("\nCurrent recipe details:")
    print(f"1. Name: {recipe_to_edit.name}")
    print(f"2. Ingredients: {recipe_to_edit.ingredients}")
    print(f"3. Cooking Time: {recipe_to_edit.cooking_time}")

    choice = input("Enter the number of the attribute you want to edit (1-3): ")
    if choice not in ['1', '2', '3']:
        print("Invalid choice.")
        return None

    if choice == '1':
        new_name = input("Enter new name (max 50 characters): ")
        while len(new_name) > 50 or not new_name.replace(' ', '').isalnum():
            new_name = input("Invalid input. Please enter a valid recipe name (max 50 characters): ")
        recipe_to_edit.name = new_name

    elif choice == '2':
        new_ingredients = input("Enter new ingredients (comma-separated): ")
        recipe_to_edit.ingredients = new_ingredients

    elif choice == '3':
        new_cooking_time = input("Enter new cooking time (in minutes): ")
        while not new_cooking_time.isnumeric():
            new_cooking_time = input("Invalid input. Please enter a valid cooking time (in minutes): ")
        recipe_to_edit.cooking_time = int(new_cooking_time)

    recipe_to_edit.calculate_difficulty()
    session.commit()
    print("Recipe updated successfully!")

def delete_recipe():
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database.")
        return None

    results = session.query(Recipe.id, Recipe.name).all()
    print("Available recipes:")
    for id, name in results:
        print(f"{id}. {name}")

    recipe_id = input("Enter the ID of the recipe you want to delete: ")
    if not recipe_id.isnumeric():
        print("Invalid input. Please enter a valid recipe ID.")
        return None

    recipe_to_delete = session.query(Recipe).filter_by(id=int(recipe_id)).first()
    if not recipe_to_delete:
        print("Recipe not found.")
        return None

    confirm = input(f"Are you sure you want to delete '{recipe_to_delete.name}'? (yes/no): ").lower()
    if confirm == 'yes':
        session.delete(recipe_to_delete)
        session.commit()
        print("Recipe deleted successfully!")
    else:
        print("Deletion cancelled.")

def main_menu():
    while True:
        print("\n==== Recipe Management System ====")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for recipes by ingredients")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print("Type 'quit' to exit the application")

        choice = input("Enter your choice: ").lower()

        if choice == '1':
            create_recipe()
        elif choice == '2':
            view_all_recipes()
        elif choice == '3':
            search_by_ingredients()
        elif choice == '4':
            edit_recipe()
        elif choice == '5':
            delete_recipe()
        elif choice == 'quit':
            print("Thank you for using the Recipe Management System. Goodbye!")
            break
        else:
            print("Invalid input. Please try again.")

    session.close()
    engine.dispose()

if __name__ == "__main__":
    main_menu()
