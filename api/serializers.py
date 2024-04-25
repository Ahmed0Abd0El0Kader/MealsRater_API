from rest_framework import serializers
from . models import *

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields  = ['id','title','description','no_of_rating','avg_rating']
        

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Rating        
        fields  = ['id','user','stars','meal']