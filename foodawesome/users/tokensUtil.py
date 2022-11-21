from rest_framework_simplejwt.tokens import RefreshToken

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
def googleGetAccessToken():
    pass

def googleValidateIdToken():
    pass