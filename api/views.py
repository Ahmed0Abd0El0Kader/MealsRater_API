from django.shortcuts import render
from rest_framework import viewsets
from . models import *
from .serializers import *

# Create your views here.

class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    queryset  = Meal.objects.all()
    
class RatingViewSet(viewsets.ModelViewSet):
    queryset  = Rating.objects.all()
    serializer_class = RatingSerializer    