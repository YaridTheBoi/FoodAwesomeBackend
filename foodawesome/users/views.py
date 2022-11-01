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
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer, ForgotPasswordSerializer, ResetPasswordSerializer

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
            link=settings.BACKEND_URL +reverse('verify-register', args=[token.key, newUser.id])
            #link='xd'
            #print(link)
            send_mail(
                subject='Register Confirmation',
                message='Token: '+ link ,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[newUser.email]
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

class VerifyRegisterView(APIView):

    def get(self, request, token, userId):
        try:
            userFromUrl=User.objects.get(id=userId)
            tokenFromUser=Token.objects.get(user=userFromUrl)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


        if(tokenFromUser.key==token):
            userFromUrl.is_active=True
            userFromUrl.save()

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)



class ForgotPasswordView(APIView):
    serializer_class=ForgotPasswordSerializer
    def post(self, request):
        serializer=ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.checkUser(request.data)
            if user is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            token, created=Token.objects.get_or_create(user=user)
            link=settings.BACKEND_URL+reverse('reset-password', args=[token.key, user.id])
            send_mail(
                subject='Reset password',
                message='Reset password link: '+ link ,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email]
            )

            return Response(status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    serializer_class=ResetPasswordSerializer
    def post(self, request, token, userId):
        serializer=ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            #print('is Valid')

            try:
                userFromUrl=User.objects.get(id=userId)
                tokenFromUser=Token.objects.get(user=userFromUrl)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if(tokenFromUser.key==token):
                
                user=serializer.changeUsersPassword(serializer.verify(request.data), userId)

                if(user is not None):
                    return Response(status=status.HTTP_200_OK)


                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)