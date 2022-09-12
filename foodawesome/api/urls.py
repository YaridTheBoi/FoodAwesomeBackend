from django.urls import path
from .views import main, RecipeList
urlpatterns = [
    path('', main),
    path('recipes/', RecipeList.as_view())      #leads to basic view
]
