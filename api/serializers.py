from core.models import Recipe, Ingredient
from rest_framework import serializers


class IngredientforRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("amount", "item")


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="tag")
    ingredients = IngredientforRecipeSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "pk",
            "author",
            "title",
            "prep_time_in_minutes",
            "cook_time_in_minutes",
            "tags",
            "public",
            "ingredients",
        )
