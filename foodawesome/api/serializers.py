
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


    def create(self, request):
        val_data=request.data
        authorId=User.objects.filter(id=request.user.id).first()
        print(authorId)
        try:
            recipe=Recipe.objects.create(author=authorId,
                                        title=val_data['title'],
                                        ingredients=val_data['ingredients'],
                                        description=val_data['description'],
                                        dish_type=val_data['dish_type'])

        except:
            return None
        
        recipe.save()

        return recipe