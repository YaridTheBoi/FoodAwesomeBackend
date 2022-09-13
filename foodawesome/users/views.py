from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings

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
