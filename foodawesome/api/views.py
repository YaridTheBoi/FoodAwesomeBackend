#other
import random

#django
from django.shortcuts import render
from django.http import HttpResponse, Http404

#api framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS


#serializers, models
from .serializers import RecipeSerializer, CreateRecipeSerializer
from .models import Recipe
from django.contrib.auth.models import User

def main(request):
    return HttpResponse("API PATH")



#=====READ ONLY PERMISSION=====
class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS




#=====BASIC VIEW=====
class RecipeList(APIView):
    permission_classes=[IsAuthenticated|ReadOnly]
    serializer_class=RecipeSerializer
    queryset=Recipe.objects.all()
    
    def get(self, request):
        recipes=Recipe.objects.all()
        serializer= RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer= CreateRecipeSerializer(data=request.data)
        if serializer.is_valid():
            recipe=serializer.create(request)
            if(recipe is not None):
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)



#=====DETAILED VIEW=====
class RecipeDetailed(APIView):
    permission_classes=[IsAuthenticated|ReadOnly]
    queryset=Recipe.objects.all()
    serializer_class=RecipeSerializer


    # This function is used to return recipe of given id or raises Http404
    def get_recipe_by_id(self, id):
        try:
            return Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            raise Http404


    def get(self, request, id):
        recipes=self.get_recipe_by_id(id)
        serializer=RecipeSerializer(recipes)
        return Response(serializer.data)
        

    def delete(self, request, id):
        recipeToRemove=self.get_recipe_by_id(id)
        requestUser=User.objects.get(id=request.user.id)
        if(recipeToRemove.author!=requestUser):
            return Response( status=status.HTTP_401_UNAUTHORIZED)
        
        recipeToRemove.delete()
        return Response(status=status.HTTP_200_OK)


    def put(self, request, id):
        serializer=CreateRecipeSerializer(data=request.data)
        recipeToEdit=Recipe.objects.get(id=id)
        requestUser=User.objects.get(id=request.user.id)

        if(recipeToEdit.author!=requestUser):
            return Response( status=status.HTTP_401_UNAUTHORIZED)

        if(serializer.is_valid()):
            editedRecipe=serializer.update(request, id)
            if(editedRecipe is None):
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#=====STATS VIEW=====
class StatsView(APIView):
    def get(self, request):
        usersAmount=User.objects.all().count()
        recipesAmount=Recipe.objects.all().count()

        response={'users': usersAmount, 'recipes':recipesAmount}
        return Response(response, status=status.HTTP_200_OK)


#=====RANDOM RECIPE VIEW=====
class RandomRecipeView(APIView):
    def get(self, request):
        allRecipesId=Recipe.objects.values_list('id', flat=True)
        randomRecipe=Recipe.objects.get(id=random.choice(allRecipesId))
        serializer=RecipeSerializer(randomRecipe)        
        return Response(serializer.data, status=status.HTTP_200_OK)
