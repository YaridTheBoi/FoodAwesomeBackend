from django.urls import path
from .views import RecipeList, main, RecipeDetailed
urlpatterns = [
    path('', main),
    path('recipes/', RecipeList.as_view()),      #leads to basic view
    path('recipes/<int:id>', RecipeDetailed.as_view())
]
