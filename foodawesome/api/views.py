#django
from django.shortcuts import render
from django.http import HttpResponse

#api framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#serializers, models
from .serializers import RecipeSerializer
from .models import Recipe


def main(request):
    return HttpResponse("API PATH")

#=====BASIC VIEW=====
class RecipeList(APIView):
    serializer_class=RecipeSerializer
    queryset=Recipe.objects.all()

    def get(self, request):
        recipes=Recipe.objects.all()
        serializer= RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer= RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)