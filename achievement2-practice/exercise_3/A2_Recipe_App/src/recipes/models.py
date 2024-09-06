from django.db import models



class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    cooking_time = models.IntegerField(help_text="Cooking time in minutes")
    ingredients = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
