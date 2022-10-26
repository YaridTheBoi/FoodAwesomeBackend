
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
    description=serializers.CharField(style={'placeholder': 'description'})
    dish_type=serializers.CharField(style={'placeholder': 'description'})
    
    extra_kwargs={'title':{'required': True}, 
                    'ingredients': {'required':True},
                    'description': {'required':True},
                    'dish_type': {'required': True}}


    def verifyType(self, type):
        if(any(type.upper() in i for i in Recipe.DISH_TYPES)):
            return type.upper()
        else:
            return 'OT'


    def create(self, request):
        val_data=request.data
        authorId=User.objects.filter(id=request.user.id).first()
        



        try:
            recipe=Recipe.objects.create(author=authorId,
                                        title=val_data['title'],
                                        ingredients=val_data['ingredients'],
                                        description=val_data['description'],
                                        dish_type=self.verifyType(val_data['dish_type']))

        except:
            return None
        
        recipe.save()

        return recipe


        


    def update(self, request, id):
        val_data=request.data
        authorId=User.objects.filter(id=request.user.id).first()
    
        try:
            recipe=Recipe.objects.filter(id=id).update(
                                            title=val_data['title'],
                                            ingredients=val_data['ingredients'],
                                            description=val_data['description'],
                                            dish_type=self.verifyType(val_data['dish_type']))
                                        
        except:
            return None



        return recipe
