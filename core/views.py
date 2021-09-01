import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Min, F, Max
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import (
    IngredientForm,
    RecipeForm,
    RecipeStepForm,
)
from .models import Recipe


def recipe_list(request):
    if not request.user.is_authenticated:
        return redirect("auth_login")
    recipes = Recipe.objects.all().order_by("title")

    template_name = "core/recipe_list.html"

    return render(request, template_name, {"recipes": recipes})


def add_recipe(request):
    if request.method == "POST":
        form = RecipeForm(data=request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, "Recipe added!")
            return redirect("recipe_list")

    else:
        form = RecipeForm()

    return render(request, "core/add_recipe.html", {"form": form})


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(
        request,
        "core/recipe_detail.html",
        {
            "recipe": recipe,
            "ingredient_form": IngredientForm(),
            "step_form": RecipeStepForm(),
        },
    )


def add_ingredient(request, recipe_pk):
    pass
