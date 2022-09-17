from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

#api framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#models
from django.contrib.auth.models import User
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer

#tokens
from .tokensUtil import getUserToken
from rest_framework.authtoken.models import Token

def main(request):
    return HttpResponse("AUTH PATH")


def send_test_mail(request):

    send_mail(
        subject='Test Mail FoodAwesome',
        message='No siema mordo',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['kacper.chrostowski@gmail.com']
    )
    return HttpResponse("MAIL SENT")


class LoginView(APIView):
    serializer_class=LoginSerializer
    def post(self, request):
        serializer=LoginSerializer(data=request.data)

        if serializer.is_valid():

            user=serializer.verify(request.data)

            if(user is None):
                return Response(status=status.HTTP_404_NOT_FOUND)

            tokens=getUserToken(user)

            return Response(tokens,status=status.HTTP_200_OK)



class RegisterView(APIView):
    serializer_class=RegisterSerializer
    queryset=User.objects.all()

    def get(self, request):

        users=User.objects.all()
        serializer= UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            newUser=serializer.create(serializer.verify(request.data))
            if(newUser is None):
                return Response(status=status.HTTP_409_CONFLICT)


            token, created=Token.objects.get_or_create(user=newUser)
            link=request.META['HTTP_HOST']+reverse('verify-register', args=[token.key, newUser.id])
            send_mail(
                subject='Register Confirmation',
                message='Token: '+ link ,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[newUser.email]
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

class VerifyRegisterView(APIView):

    def get(self, request, token, user_id):
        userFromUrl=User.objects.get(id=user_id)
        tokenFromUser=Token.objects.get(user=userFromUrl)

        if(tokenFromUser.key==token):
            userFromUrl.is_active=True
            userFromUrl.save()

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)