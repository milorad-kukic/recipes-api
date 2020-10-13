from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


def create_user(email, password, first_name='', last_name=''):
    return get_user_model().objects.create_user(email, password, first_name=first_name, last_name=last_name)


def create_superuser(email, password):
    return get_user_model().objects.create_superuser(email, password)



class AdminSiteTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.admin_user = create_superuser('admin@site.com', 'testpassword123')
        self.client.force_login(self.admin_user)
        self.user = create_user(
            email='user@site.com', 
            password='randompassword',
            first_name='Milorad',
            last_name='Kukic'
        )

    def test_users_page_lists_users(self):
        ADMIN_USERS_PAGE = reverse('admin:recipes_user_changelist')

        res = self.client.get(ADMIN_USERS_PAGE)

        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.first_name)
        self.assertContains(res, self.user.last_name)

    def test_user_change_page_rendered_correctly(self):
        EDIT_USER_PAGE_URL = reverse('admin:recipes_user_change', args=[self.user.id])

        res = self.client.get(EDIT_USER_PAGE_URL)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page_renders_correctly(self):
        CREATE_USER_PAGE_URL = reverse('admin:recipes_user_add')

        res = self.client.get(CREATE_USER_PAGE_URL)

        self.assertEqual(res.status_code, 200)
