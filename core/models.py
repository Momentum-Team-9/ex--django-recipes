from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.constraints import UniqueConstraint
from ordered_model.models import OrderedModel


class User(AbstractUser):
    def __str__(self):
        return self.username


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    title = models.CharField(max_length=255)
    prep_time_in_minutes = models.PositiveIntegerField(null=True, blank=True)
    cook_time_in_minutes = models.PositiveIntegerField(null=True, blank=True)
    original_recipe = models.ForeignKey(
        to="self", on_delete=models.SET_NULL, null=True, blank=True
    )
    public = models.BooleanField(default=True)
    favorited_by = models.ManyToManyField(
        User, related_name="favorite_recipes", blank=True
    )

    def total_time_in_minutes(self):
        if self.cook_time_in_minutes is None or self.prep_time_in_minutes is None:
            return None
        return self.cook_time_in_minutes + self.prep_time_in_minutes

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="ingredients"
    )
    amount = models.CharField(max_length=20)
    item = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.amount} {self.item}"


class RecipeStep(OrderedModel):
    recipe = models.ForeignKey(
        to=Recipe, on_delete=models.CASCADE, related_name="steps"
    )
    text = models.TextField()
    order_with_respect_to = "recipe"

    def __str__(self):
        return f"{self.order} {self.text}"


class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meal_plans")
    date = models.DateField(verbose_name="Date for plan")
    recipes = models.ManyToManyField(to=Recipe, related_name="meal_plans")

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "date"], name="unique_user_date")
        ]
