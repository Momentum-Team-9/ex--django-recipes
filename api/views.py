from django.shortcuts import render
from rest_framework import serializers, viewsets
from core.models import Recipe
from .serializers import RecipeSerializer

# Create your views here.
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
