from django.urls import path
from .views import RecipeList, main, RecipeDetailed, StatsView, RandomRecipeView
urlpatterns = [
    path('', main),
    path('recipes/', RecipeList.as_view()),      #leads to basic view
    path('recipes/<int:id>', RecipeDetailed.as_view()),
    path('recipes/stats', StatsView.as_view()),
    path('recipes/random', RandomRecipeView.as_view())
]
