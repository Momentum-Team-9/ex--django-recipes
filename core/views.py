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
            return redirect("recipe_detail", pk=recipe.pk)

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
    recipe = get_object_or_404(request.user.recipes, pk=recipe_pk)

    if request.method == "POST":
        form = IngredientForm(data=request.POST)

        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.recipe = recipe
            ingredient.save()

    return redirect("recipe_detail", pk=recipe.pk)


@login_required
def show_meal_plan(request, year=None, month=None, day=None):
    """
    Given a year, month, and day, look up the meal plan for the current user for that
    day and display it.

    If a form is submitted to add a recipe, then go ahead and add recipe to the
    meal plan for that day.
    """
    if year is None:
        date_for_plan = datetime.date.today()
    else:
        date_for_plan = datetime.date(year, month, day)
    next_day = date_for_plan + datetime.timedelta(days=1)
    prev_day = date_for_plan + datetime.timedelta(days=-1)

    # https://docs.djangoproject.com/en/3.0/ref/models/querysets/#get-or-create
    meal_plan, _ = request.user.meal_plans.get_or_create(date=date_for_plan)
    # meal_plan, _ = MealPlan.objects.get_or_create(user=request.user, date=date_for_plan)
    recipes = Recipe.objects.for_user(request.user).exclude(
        pk__in=[r.pk for r in meal_plan.recipes.all()]
    )

    return render(
        request,
        "core/show_mealplan.html",
        {
            "plan": meal_plan,
            "recipes": recipes,
            "date": date_for_plan,
            "next_day": next_day,
            "prev_day": prev_day,
        },
    )


@login_required
@csrf_exempt
def meal_plan_add_remove_recipe(request):
    date = request.POST.get("date")
    recipe_pk = request.POST.get("pk")
    action = request.POST.get("action")

    meal_plan, _ = request.user.meal_plans.get_or_create(date=date)
    recipe = Recipe.objects.for_user(request.user).get(pk=recipe_pk)

    if action == "add":
        meal_plan.recipes.add(recipe)
    elif action == "remove":
        meal_plan.recipes.remove(recipe)

    return HttpResponse(status=204)
