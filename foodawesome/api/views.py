#django
from django.shortcuts import render
from django.http import HttpResponse

#api framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


#serializers, models
from .serializers import RecipeSerializer, CreateRecipeSerializer
from .models import Recipe


def main(request):
    return HttpResponse("API PATH")

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
        print(request.data)
        if serializer.is_valid():
            recipe=serializer.create(request)
            if(recipe is not None):
                return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    