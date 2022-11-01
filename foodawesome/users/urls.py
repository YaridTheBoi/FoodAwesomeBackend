from django.urls import path
from .views import main, send_test_mail, LoginView, RegisterView, VerifyRegisterView, ForgotPasswordView, ResetPasswordView

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
    path('login', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('verify-register/<str:token>/<int:userId>', VerifyRegisterView.as_view(), name='verify-register'),
    path('forgot-password', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<str:token>/<int:userId>', ResetPasswordView.as_view(), name='reset-password')


]
