from django.urls import path
from .views import main, send_test_mail, LoginView, RegisterView

from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('', main),
    path('testMail', send_test_mail),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('token/verify', TokenVerifyView.as_view()),
    path('login', LoginView.as_view()),
    path('register', RegisterView.as_view()),
]
