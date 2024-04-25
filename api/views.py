from django.shortcuts import render
from rest_framework import viewsets ,status
from rest_framework.decorators import action
from rest_framework.response import Response
from . models import *
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny ,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset  = User.objects.all()
    # authentication_classes = [TokenAuthentication]  
    permission_classes = [AllowAny]

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        token,created = Token.objects.get_or_create(user = serializer.instance)
        
        return Response({'token':token.key,},status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        return Response({'message':'You can\'t create rating like this '})


class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    queryset  = Meal.objects.all()
    authentication_classes = [TokenAuthentication]  
    permission_classes = [IsAuthenticated]  
    
    @action(methods = ['POST'],detail = True)
    def rate_meal(self,request,pk = None ):
        if 'stars' in request.data:
            '''create or update'''
            meal = Meal.objects.get(pk=pk)
            user = request.user
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
    authentication_classes = [TokenAuthentication]  
    permission_classes = [IsAuthenticated]  
    
    
    def update(self, request, *args, **kwargs):
        return Response({'message':'This is not how you should create and update '},status=status.HTTP_400_BAD_REQUEST)
    def create(self, request, *args, **kwargs):
        return Response({'message':'This is not how you should create and update '},status=status.HTTP_400_BAD_REQUEST)