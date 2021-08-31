import datetime

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
    recipes = Recipe.objects.all().order_by("title")

    if request.is_ajax():
        template_name = "core/_recipe_list.html"
    else:
        template_name = "core/recipe_list.html"

    return render(request, template_name, {"recipes": recipes})
