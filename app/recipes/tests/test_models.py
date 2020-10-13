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
    
    def test_create_user_email_is_normalized(self):
        """ To normalize email means that all letters in domain are lowwercased """
        email = 'TestEmail@SomeDomain.com'

        user = get_user_model().objects.create_user(
            email=email,
            password='AnyRandomPassword'
        )

        self.assertEqual(user.email, 'TestEmail@somedomain.com')

    def test_create_user_with_no_email_raises_error(self):
        expected_msg = 'User must have an email address'
        with self.assertRaisesMessage(ValueError, expected_msg):
            get_user_model().objects.create_user(None, 'password123')

