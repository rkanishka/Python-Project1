import mysql.connector
from mysql.connector import Error

# Establish database connection
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='cf-ipython',
            passwd='password'
        )
        cursor = conn.cursor()

        # Create database if not exists
        cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
        cursor.execute("USE task_database")

        # Drop the table if it exists to ensure the correct structure
        cursor.execute("DROP TABLE IF EXISTS Recipes")

        # Create table with AUTO_INCREMENT for id
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Recipes(
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50),
                ingredients VARCHAR(255),
                cooking_time INT,
                difficulty VARCHAR(20)
            );
        ''')
        return conn, cursor
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        exit(1)

def create_recipe(conn, cursor):
    print("\n --CREATE NEW RECIPE--")
    name = input("Enter name of recipe: ")
    try:
        cooking_time = int(input("Enter cooking time (in minutes): "))
    except ValueError:
        print("Invalid input for cooking time. Please enter a number.")
        return

    ingredients = input("Enter ingredients (comma-separated): ").split(',')
    ingredients = [ingredient.strip() for ingredient in ingredients]

    difficulty = calculate_difficulty(cooking_time, ingredients)
    ingredients_str = ", ".join(ingredients)

    try:
        query = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, ingredients_str, cooking_time, difficulty))
        conn.commit()
        print("Recipe created successfully!")
    except Error as e:
        print(f"Error creating recipe: {e}")

def calculate_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        return "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        return "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        return "Intermediate"
    else:
        return "Hard"

def search_recipe(conn, cursor):
    print("\n--- Search for a Recipe ---")
    try:
        cursor.execute("SELECT DISTINCT ingredients FROM Recipes")
        results = cursor.fetchall()
        all_ingredients = set()
        for row in results:
            ingredients = row[0].split(", ")
            all_ingredients.update(ingredients)

        if not all_ingredients:
            print("No ingredients found. Please add some recipes first.")
            return

        print("Available ingredients:")
        for i, ingredient in enumerate(sorted(all_ingredients), 1):
            print(f"{i}. {ingredient}")

        choice = input("Enter the number of the ingredient to search for: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(all_ingredients):
                search_ingredient = sorted(all_ingredients)[choice - 1]
                query = "SELECT * FROM Recipes WHERE ingredients LIKE %s"
                cursor.execute(query, (f"%{search_ingredient}%",))
                recipes = cursor.fetchall()

                if recipes:
                    print("\nMatching recipes:")
                    for recipe in recipes:
                        print(f"ID: {recipe[0]}, Name: {recipe[1]}, Ingredients: {recipe[2]}, Cooking Time: {recipe[3]}, Difficulty: {recipe[4]}")
                else:
                    print("No recipes found with that ingredient.")
            else:
                print("Invalid choice. Please select a valid ingredient number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    except Error as e:
        print(f"Error searching for recipe: {e}")

def update_recipe(conn, cursor):
    print("\n--- Update a Recipe ---")
    try:
        cursor.execute("SELECT id, name FROM Recipes")
        recipes = cursor.fetchall()
        
        if not recipes:
            print("No recipes found. Please add some recipes first.")
            return

        print("Available recipes:")
        for recipe in recipes:
            print(f"ID: {recipe[0]}, Name: {recipe[1]}")

        try:
            recipe_id = int(input("Enter the ID of the recipe to update: "))
        except ValueError:
            print("Invalid input for recipe ID. Please enter a number.")
            return

        column = input("Enter the column to update (name/cooking_time/ingredients): ")
        new_value = input("Enter the new value: ")

        try:
            if column == 'cooking_time':
                new_value = int(new_value)
                cursor.execute("SELECT ingredients FROM Recipes WHERE id = %s", (recipe_id,))
                ingredients = cursor.fetchone()[0].split(", ")
                new_difficulty = calculate_difficulty(new_value, ingredients)
                query = f"UPDATE Recipes SET {column} = %s, difficulty = %s WHERE id = %s"
                cursor.execute(query, (new_value, new_difficulty, recipe_id))
            elif column == 'ingredients':
                new_value = ', '.join([ingredient.strip() for ingredient in new_value.split(',')])
                query = f"UPDATE Recipes SET {column} = %s WHERE id = %s"
                cursor.execute(query, (new_value, recipe_id))
                cursor.execute("SELECT cooking_time, ingredients FROM Recipes WHERE id = %s", (recipe_id,))
                result = cursor.fetchone()
                cooking_time = result[0]
                ingredients = result[1].split(", ")
                new_difficulty = calculate_difficulty(cooking_time, ingredients)
                cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (new_difficulty, recipe_id))
            else:
                query = f"UPDATE Recipes SET {column} = %s WHERE id = %s"
                cursor.execute(query, (new_value, recipe_id))

            conn.commit()
            print("Recipe updated successfully!")
        except ValueError:
            print("Invalid input. Please enter a valid value.")
    except Error as e:
        print(f"Error updating recipe: {e}")

def delete_recipe(conn, cursor):
    print("\n--- Delete a Recipe ---")
    try:
        cursor.execute("SELECT id, name FROM Recipes")
        recipes = cursor.fetchall()
        
        if not recipes:
            print("No recipes found. Please add some recipes first.")
            return

        print("Available recipes:")
        for recipe in recipes:
            print(f"ID: {recipe[0]}, Name: {recipe[1]}")

        try:
            recipe_id = int(input("Enter the ID of the recipe to delete: "))
        except ValueError:
            print("Invalid input for recipe ID. Please enter a number.")
            return

        query = "DELETE FROM Recipes WHERE id = %s"
        cursor.execute(query, (recipe_id,))
        conn.commit()

        if cursor.rowcount > 0:
            print("Recipe deleted successfully!")
        else:
            print("No recipe found with that ID.")
    except Error as e:
        print(f"Error deleting recipe: {e}")

def main_menu(conn, cursor):
    while True:
        print("\n===== Recipe Management System =====")
        print("1. Create a new recipe")
        print("2. Search for a recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice == '5':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

    # Commit any remaining changes to the database
    conn.commit()

# Main script
if __name__ == "__main__":
    conn, cursor = connect_to_database()
    try:
        main_menu(conn, cursor)
    except Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed")