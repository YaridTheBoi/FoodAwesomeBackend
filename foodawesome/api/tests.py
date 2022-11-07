from itertools import count
from types import new_class
from urllib import response
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Recipe

class TestApi(APITestCase):

    def setUp(self):
        user=User.objects.create_user("testusername", 'mail@mail.com', 'testpassword')
        recipe=Recipe.objects.create(author=user,
                                        title='test recipe',
                                        ingredients='test ingredients',
                                        description='test description',
                                        dish_type='OT')


    def authenticate(self):
        sample_login={'login': ['mail@mail.com'], 'password':['testpassword']}
        response=self.client.post(reverse('login'), sample_login)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")


    def authenticateExpiredOrWrong(self):
        sample_login={'login': ['mail@mail.com'], 'password':['testpassword']}
        response=self.client.post(reverse('login'), sample_login)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']} zesralem sie")


    def test_get_recipes_without_auth_should_be_200(self):
        response=self.client.get(reverse('recipes'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_recipes_with_auth_should_be_200(self):
        self.authenticate()
        response=self.client.get(reverse('recipes'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_recipes_with_wrong_auth_should_be_401(self):
        self.authenticateExpiredOrWrong()
        response=self.client.get(reverse('recipes'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_post_recipes_without_auth_should_be_401(self):
        count_before=Recipe.objects.count()
        sample_recipe={'title': ['test no auth'], 'ingredients': ['ingredients no auth'], 'description': ['desc no auth'], 'dish_type': ['OT']}
        response= self.client.post(reverse('recipes'), sample_recipe)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(count_before, Recipe.objects.count())


    def test_post_recipes_with_expired_auth_should_be_401(self):
        self.authenticateExpiredOrWrong()
        count_before=Recipe.objects.count()
        sample_recipe={'title': ['test auth'], 'ingredients': ['ingredients auth'], 'description': ['desc auth'], 'dish_type': ['OT']}
        response= self.client.post(reverse('recipes'), sample_recipe)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(count_before, Recipe.objects.count())


    def test_post_recipes_with_auth_should_be_201(self):
        self.authenticate()
        count_before=Recipe.objects.count()
        sample_recipe={'title': ['test auth'], 'ingredients': ['ingredients auth'], 'description': ['desc auth'], 'dish_type': ['OT']}
        response= self.client.post(reverse('recipes'), sample_recipe)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(count_before+1, Recipe.objects.count())


    def test_post_recipes_with_incomplete_data_should_be_400(self):
        self.authenticate()
        count_before=Recipe.objects.count()
        sample_no_title_recipe={'ingredients': ['ingredients auth'], 'description': ['desc auth'], 'dish_type': ['OT']}
        response= self.client.post(reverse('recipes'), sample_no_title_recipe)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(count_before, Recipe.objects.count())


    def test_post_recipes_with_wrong_dish_type_should_create_dish_with_type_OT(self):
        self.authenticate()
        count_before=Recipe.objects.count()
        sample_no_title_recipe={'title': ['test auth'], 'ingredients': ['ingredients auth'], 'description': ['desc auth'], 'dish_type': ['unacceptable data']}
        response= self.client.post(reverse('recipes'), sample_no_title_recipe)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(count_before+1, Recipe.objects.count())
        new_recipe=Recipe.objects.get(title= 'test auth')
        self.assertEqual(new_recipe.dish_type, 'OT')


    def test_get_stats_with_auth_should_be_200(self):
        self.authenticate()
        count_users=User.objects.count()
        count_recipes=Recipe.objects.count()
        response=self.client.get(reverse('recipe-stats'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['users'], count_users)
        self.assertEqual(response.data['recipes'], count_recipes)


    def test_get_stats_with_no_auth_should_be_200(self):
        count_users=User.objects.count()
        count_recipes=Recipe.objects.count()
        response=self.client.get(reverse('recipe-stats'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['users'], count_users)
        self.assertEqual(response.data['recipes'], count_recipes)


    def test_get_stats_with_wrong_auth_should_be_401(self):
        self.authenticateExpiredOrWrong()
        count_users=User.objects.count()
        count_recipes=Recipe.objects.count()
        response=self.client.get(reverse('recipe-stats'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
