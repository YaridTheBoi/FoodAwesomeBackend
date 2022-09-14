from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.mail import send_mail
from django.conf import settings

#api framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

#models
from django.contrib.auth.models import User
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


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

            myRequest=HttpRequest()
            myRequest.method="POST"

            payload={'username': user.get_username, 'password':request.data['']}

            print(payload)



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
            return Response(serializer.data, status=status.HTTP_201_CREATED)