from rest_framework_simplejwt.tokens import RefreshToken

# function used to return new access token for user
def getUserToken(user):
    refresh=RefreshToken.for_user(user)

    return{
        'access':str(refresh.access_token)
    }

