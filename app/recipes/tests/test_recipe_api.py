from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


RECIPES_URL = reverse('recipes:recipe-list')


class PublicRecipeApi(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_recipes_should_return_401_if_user_not_authenticated(self):
        res = self.client.get(RECIPES_URL)
        
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
