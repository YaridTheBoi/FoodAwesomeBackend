from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.http import HttpResponse
import requests
from django.core.exceptions import ValidationError

GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'



# function used to return new access token for user
def getUserToken(user):
    refresh=RefreshToken.for_user(user)

    return{
        'access':str(refresh.access_token)
    }




# https://github.com/HackSoftware/Django-React-GoogleOauth2-Example/blob/main/server/auth/services.py
def googleGetAccessToken(code, redirect_uri):
    data={
        'code':code,
        'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
        'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

    if not response.ok:
        raise ValidationError('Failed to get access token from google')

    return response.data['access_token']



def googleValidateIdToken(token):
    response = requests.get(
        GOOGLE_ID_TOKEN_INFO_URL,
        params={'id_token': token}
    )
    if not response.ok:
        raise ValidationError('invalid token')

    aud=response.data['aud']

    if(aud != settings.GOOGLE_OAUTH2_CLIENT_ID):
        raise ValidationError("Invalid aud")
    return True