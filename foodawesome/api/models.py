from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Recipe(models.Model):
    title=models.CharField(max_length=100, null=False)
    ingredients=models.TextField(null=False)
    description=models.TextField(null=False)
    
    #======THIS IS REMOVED FOR EARLY DEVELOPMENT, WILL COME BACK SOON======="
    #author=models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    
    create_date=models.DateField(auto_now_add=True)
    

    #=====CODE BELOW ALLOWS TO EASILY PICK DISH TYPE=====
    DISH_TYPES=(
        ('BF', 'Breakfast'),
        ('LU', 'Lunch'),
        ('DN', 'Dinner'),
        ('DE', 'Dessert'),
        ('OT', 'Other'),
    )

    dish_type=models.CharField(max_length=2, choices=DISH_TYPES, 
                                default='OT' )
