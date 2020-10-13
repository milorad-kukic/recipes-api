from django.test import TestCase
from django.contrib.auth import get_user_model


class TestUser(TestCase):

    def test_can_create_user_with_email_as_username(self):
        email = 'test@email.com'
        password = 'TestPass123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
