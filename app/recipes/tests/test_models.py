from django.test import TestCase
from django.contrib.auth import get_user_model

from recipes.models import Recipe


class TestUser(TestCase):

    def test_create_user_with_email_as_username_successfull(self):
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

    def test_create_superuser_sets_staff_and_super_user_flags(self):
        user = get_user_model().objects.create_superuser(
            email='user@mail.com',
            password='anypassword'
        )
        
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

class TestRecipe(TestCase):

    def test_recipe_is_represented_by_name(self):
        recipe = Recipe.objects.create(
            name='Burger', 
            image_path='some path', 
            description='Tasty burger'
        )

        self.assertEqual(str(recipe), recipe.name)
