from random import sample
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.conf import settings

class TestAuth(APITestCase):
    
    def setUp(self):
        user=User.objects.create_user("testusername", 'mail@mail.com', 'testpassword')



    def test_login_with_wrong_data_should_be_404(self):
        sample_login={'login':'nie_ma_takiego_usera', 'password':'takie_haslo_nie_istnieje'}
        response=self.client.post(reverse('login'), sample_login)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    
    
    def test_login_with_existing_data_by_username_should_be_200(self):
        sample_login={'login': ['testusername'], 'password':['testpassword']}
        response=self.client.post(reverse('login'), sample_login)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_login_with_existing_data_by_email_should_be_200(self):
        sample_login={'login': ['mail@mail.com'], 'password':['testpassword']}
        response=self.client.post(reverse('login'), sample_login)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_register_create_new_user_should_be_201(self):
        sample_register={'username':['newuser'], 'email':['newmail@mail.com'], 'password':['password123'], 'repeatPassword':['password123']}
        response=self.client.post(reverse('register'), sample_register)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        



    def test_register_create_user_with_same_data_as_existing_should_be_409(self):
        sample_register={'username':['testusername'], 'email':['mail@mail.com'], 'password':['testpassword'], 'repeatPassword':['testpassword']}
        response=self.client.post(reverse('register'), sample_register)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)



    def test_register_create_user_with_two_different_passwords_should_be_409(self):
        sample_register={'username':['newuser'], 'email':['newmail@mail.com'], 'password':['password123'], 'repeatPassword':['achujci']}
        response=self.client.post(reverse('register'), sample_register)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


    def test_register_create_user_affects_db_should_be_true(self):
        users_amount_before=User.objects.count()
        sample_register={'username':['newuser'], 'email':['newmail@mail.com'], 'password':['password123'], 'repeatPassword':['password123']}
        response=self.client.post(reverse('register'), sample_register)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), users_amount_before+1)



    def test_verify_register_should_be_200(self):
        user=User.objects.get(username='testusername')
        token, created=Token.objects.get_or_create(user=user)
        link=settings.BACKEND_URL +reverse('verify-register', args=[token.key, user.id])
        response=self.client.get(link)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_verify_register_with_wrong_url_should_be_404(self):
        user=User.objects.get(username='testusername')
        token, created=Token.objects.get_or_create(user=user)
        link=settings.BACKEND_URL +reverse('verify-register', args=[token.key, 999999999999999])
        response=self.client.get(link)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_forgot_password_for_existing_user_should_be_200(self):
        sample_forgot_password={'email': ['mail@mail.com']}
        response=self.client.post(reverse('forgot-password'), sample_forgot_password)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_forgot_password_for_not_existing_user_should_be_404(self):
        sample_forgot_password={'email': ['dontexist@mail.com']}
        response=self.client.post(reverse('forgot-password'), sample_forgot_password)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_reset_password_should_be_200(self):
        user=User.objects.get(username='testusername')
        token, created=Token.objects.get_or_create(user=user)
        link=settings.BACKEND_URL +reverse('reset-password', args=[token.key, user.id])
        sample_reset_password={'newPassword':['newpass'], 'repeatNewPassword':['newpass']}
        response=self.client.post(link, sample_reset_password)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_reset_password_with_bad_link_should_be_404(self):
        user=User.objects.get(username='testusername')
        token, created=Token.objects.get_or_create(user=user)
        link=settings.BACKEND_URL +reverse('reset-password', args=[token.key, 999999999999999])
        sample_reset_password={'newPassword':['newpass'], 'repeatNewPassword':['newpass']}
        response=self.client.post(link, sample_reset_password)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    
    def test_reset_password_with_different_passwords_should_be_400(self):
        user=User.objects.get(username='testusername')
        token, created=Token.objects.get_or_create(user=user)
        link=settings.BACKEND_URL +reverse('reset-password', args=[token.key, user.id])
        sample_reset_password={'newPassword':['newpass'], 'repeatNewPassword':['newpassalenie']}
        response=self.client.post(link, sample_reset_password)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)