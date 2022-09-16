from rest_framework_simplejwt.tokens import RefreshToken

# function used to return new refresh and access token for user
def getUserToken(user):
    refresh=RefreshToken.for_user(user)

    return{
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }