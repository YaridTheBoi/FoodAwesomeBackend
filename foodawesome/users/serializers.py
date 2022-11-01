import email
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


#=====LOGIN SERIALIZER=====
class LoginSerializer(serializers.Serializer):
    login=serializers.CharField(style={'placeholder': 'Username or Email'})
    password=serializers.CharField(
        style= {'placeholder': 'Password', 'input_type':'password'}
    )


    # Function used to verify login. Returns User if valid
    def verify(self, data):

        
        # Try to verify user with login data being username
        user=authenticate(username=data['login'], password=data['password'])
        #print(user)
        # If user is None given login might be email
        if user is None: 
            # Try to find user by email
            try:
                userFromMail=User.objects.get(email=data['login'])
            except:
                return None
            
            # Try to verify user with data from email
            user=authenticate(username=userFromMail.username, password=data['password'])

        return user


#=====REGISTER SERIALIZER====
class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField(style={'placeholder': 'Username'})
    email=serializers.CharField(style={'placeholder': 'Email'})
    password=serializers.CharField(
        style= {'placeholder': 'Password', 'input_type':'password'}
    )
    repeatPassword=serializers.CharField(
        style= {'placeholder': 'Repeat Password', 'input_type':'password'}
    )

    #Checks if password and repeatPassword are same value (in case frontend fucks up)
    def verify(self, data):
        if(data['password']!=data['repeatPassword']):
            return serializers.ValidationError({'password': 'passwords aren\'t the same'})
        
        return data


    #Create new user and return it
    def create(self, val_data):
        try:
            user=User.objects.create(username=val_data['username'],
                                    email=val_data['email'],
                                    is_active=False)     #change it later

            user.set_password(val_data['password'])
            user.save()

            return user
        except:
            return None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username', 'is_active')

class ForgotPasswordSerializer(serializers.Serializer):
    email=serializers.CharField(style={'placeholder': 'Email'})

    #Checks if user of given email exist and if so return it's object
    def checkUser(self, data):
        try:
            user=User.objects.get(email=data['email'])
        except:
            return None
        
        return user


class ResetPasswordSerializer(serializers.Serializer):
    newPassword=serializers.CharField(
        style= {'placeholder': 'New Password', 'input_type':'password'}
    )
    repeatNewPassword=serializers.CharField(
        style= {'placeholder': 'Repeat New Password', 'input_type':'password'}
    )

    def verify(self, data):
        if(data['newPassword']!=data['repeatNewPassword']):
            return None
        return data

    def changeUsersPassword(self, data, userId):
        if data is None:
            return None

        user=User.objects.get(id=userId)

        #===DEV ONLY===
        if user is None:
            print("Cholera powinno wyjsc inaczej")
            return None

        user.set_password(data['newPassword'])
        user.save()

        return user