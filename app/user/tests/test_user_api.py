from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create(**params)


class PublicUserApiTests(TestCase):
    """ Tests the users API for non authenticated users """

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        payload = {
            'email': 'new_user@mail.com',
            'password': 'testpass',
            'first_name': 'John',
            'last_name': 'Doe'
        }

        
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_users_with_existing_email_fails(self):
        payload = {
            'email': 'user@site.com',
            'password': 'sometestpass'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_password_must_be_more_than_5_characters(self):
        payload = {
            'email': 'user@site.com', 
            'password': 'pw'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
                email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_login_with_valid_credentials_should_return_token(self):
        payload = {'email': 'user@site.com', 'password': 'secretpass'}
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_login_invalid_password_doesnt_create_token(self):
        create_user(email='user@recipes.com', password='testpass')
        payload = { 'email': 'user@recipes.com', 'password': 'wrong'}

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_login_user_not_exist_token_not_created(self):
        payload = { 'email': 'user@recipes.com', 'password': 'testpass'}

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_login_empty_password_returns_error(self):
        res = self.client.post(TOKEN_URL, {'email': 'test@mail.com', 'password': ''})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
