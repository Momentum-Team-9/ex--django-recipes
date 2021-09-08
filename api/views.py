from django.shortcuts import render
from rest_framework import serializers, viewsets
from core.models import Recipe

# Create your views here.
class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
