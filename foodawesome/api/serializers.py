from dataclasses import field
from rest_framework import serializers
from .models import Recipe
from django.contrib.auth.models import User


#=====BASIC SERIALIZER USED FOR EVERYTHING=====
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Recipe
        fields=('id', 'title', 'ingredients', 'description','dish_type',
                'author', 'create_date')


#=====SERIALIZER THAT WILL BE USED IN POST AND PUT METHODS, USED TO MODIFY DATA AVAILABLE TO USER=====
class CreateRecipeSerializer(serializers.Serializer):
    title=serializers.CharField(style={"placeholder": "Title"})
    ingredients=serializers.CharField(style={"placeholder": "Ingredients"})
    extra_kwargs={'title':{'required': True}, 
                    'ingredients': {'required':True},
                    'description': {'required':True},
                    'dish_type': {'required': True}}