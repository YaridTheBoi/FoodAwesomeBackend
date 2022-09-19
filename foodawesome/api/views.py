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


def main(request):
    return HttpResponse("API PATH")

#=====READ ONLY PERMISSION=====
class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS




#=====BASIC VIEW=====
class RecipeList(APIView):
    permission_classes=[IsAuthenticated]
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
                return Response(serializer.data)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)




class RecipeDetailed(APIView):
    permission_classes=[IsAuthenticated]
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
        recipe=self.get_recipe_by_id(id)
        recipe.delete()
        return Response(status=status.HTTP_200_OK)


    def put(self, request, id):
        recipe=self.get_recipe_by_id(id)
        serializer=RecipeSerializer(recipe, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

