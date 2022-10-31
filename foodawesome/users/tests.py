from random import sample
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User


class TestAuth(APITestCase):
    '''
    def test_login_with_wrong_data(self):
        sample_login={'login':'nie_ma_takiego_usera', 'password':'takie_haslo_nie_istnieje'}
        response=self.client.post(reverse('login'), sample_login)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    '''
    
    def test_login_with_existing_data(self):
        sample_login={'login': "Yarid", 'password':"haslo123"}
        response=self.client.post(reverse('login'), sample_login)
        self.assertEqual(response.status_code, status.HTTP_200_OK)