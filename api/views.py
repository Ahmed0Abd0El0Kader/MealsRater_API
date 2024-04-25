from django.shortcuts import render
from rest_framework import viewsets ,status
from rest_framework.decorators import action
from rest_framework.response import Response
from . models import *
from .serializers import *
from django.contrib.auth.models import User
# Create your views here.

class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    queryset  = Meal.objects.all()
    
    @action(methods = ['POST'],detail = True)
    def rate_meal(self,request,pk = None ):
        if 'stars' in request.data:
            '''create or update'''
            meal = Meal.objects.get(pk=pk)
            user = User.objects.get(username = request.data['username'])
            stars = request.data['stars']
            
            try:
                #update
                rate = Rating.objects.get(user = user.id , meal = meal.id) #Specific rate
                rate.stars = stars
                rate.save()
                serializer = RatingSerializer(rate,many = False)
                json = {
                    "message":'Meal Rate Updated',
                    "result": serializer.data
                }
                return Response(json,status=status.HTTP_202_ACCEPTED)
                
            except:
                #create
                rate = Rating.objects.create(stars = stars , meal = meal , user = user)
                serializer = RatingSerializer(rate,many = False)
                json = {
                    "message":'Meal Rate Created',
                    "result": serializer.data
                }
                return Response(json,status=status.HTTP_201_CREATED)
        else:    
            return Response({"message":"Stars not Provided"},status= status.HTTP_400_BAD_REQUEST)
        
    
    
class RatingViewSet(viewsets.ModelViewSet):
    queryset  = Rating.objects.all()
    serializer_class = RatingSerializer    