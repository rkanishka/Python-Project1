from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Recipe

class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(
            name="Test Recipe",
            cooking_time=30,
            ingredients="Ingredient 1, Ingredient 2",
            description="This is a test recipe description."
        )

    def test_recipe_creation(self):
        recipe = Recipe.objects.get(recipe_id=1)
        self.assertTrue(isinstance(recipe, Recipe))
        self.assertEqual(recipe.__str__(), recipe.name)

    def test_name_max_length(self):
        recipe = Recipe.objects.get(recipe_id=1)
        max_length = recipe._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_cooking_time_help_text(self):
        recipe = Recipe.objects.get(recipe_id=1)
        help_text = recipe._meta.get_field('cooking_time').help_text
        self.assertEqual(help_text, "Cooking time in minutes")

    def test_recipe_ordering(self):
        Recipe.objects.create(name="Another Recipe", cooking_time=45, ingredients="Ingredient 3, Ingredient 4", description="Another test recipe.")
        recipes = Recipe.objects.all()
        self.assertEqual(recipes[0].name, "Another Recipe")
        self.assertEqual(recipes[1].name, "Test Recipe")

    def test_recipe_fields(self):
        recipe = Recipe.objects.get(recipe_id=1)
        self.assertEqual(recipe.name, "Test Recipe")
        self.assertEqual(recipe.cooking_time, 30)
        self.assertEqual(recipe.ingredients, "Ingredient 1, Ingredient 2")
        self.assertEqual(recipe.description, "This is a test recipe description.")

   

    def test_blank_name(self):
        with self.assertRaises(ValidationError):
            recipe = Recipe(
                name="",
                cooking_time=30,
                ingredients="Test",
                description="Test"
            )
            recipe.full_clean()

    def test_auto_increment_recipe_id(self):
        recipe1 = Recipe.objects.get(recipe_id=1)
        recipe2 = Recipe.objects.create(
            name="Second Recipe",
            cooking_time=45,
            ingredients="Ingredient 5, Ingredient 6",
            description="Second test recipe description."
        )
        self.assertEqual(recipe1.recipe_id, 1)
        self.assertEqual(recipe2.recipe_id, 2)