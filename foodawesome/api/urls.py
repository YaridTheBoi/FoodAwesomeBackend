from django.urls import path
from .views import RecipeList, main, RecipeDetailed, StatsView, RandomRecipeView
urlpatterns = [
    path('', main),
    path('recipes/', RecipeList.as_view(), name='recipes'),      #leads to basic view
    path('recipes/<int:id>', RecipeDetailed.as_view(), name='recipes-detailed'),
    path('recipes/stats', StatsView.as_view(), name='recipe-stats'),
    path('recipes/random', RandomRecipeView.as_view(), name='random-recipe')
]
