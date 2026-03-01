from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User


class UserRegistrationTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')

    def test_user_registration_success(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')
        self.assertEqual(User.objects.get().email, 'test@example.com')
        self.assertEqual(User.objects.get().role, 'user')

    def test_user_registration_with_admin_role(self):
        data = {
            'username': 'adminuser',
            'email': 'admin@example.com',
            'password': 'AdminPass123',
            'role': 'admin'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get().role, 'admin')

    def test_user_registration_duplicate_username(self):
        User.objects.create_user(
            username='testuser',
            email='first@example.com',
            password='TestPass123'
        )
        data = {
            'username': 'testuser',
            'email': 'second@example.com',
            'password': 'TestPass123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_duplicate_email(self):
        User.objects.create_user(
            username='user1',
            email='test@example.com',
            password='TestPass123'
        )
        data = {
            'username': 'user2',
            'email': 'test@example.com',
            'password': 'TestPass123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_missing_username(self):
        data = {
            'email': 'test@example.com',
            'password': 'TestPass123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_missing_email(self):
        data = {
            'username': 'testuser',
            'password': 'TestPass123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_missing_password(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_invalid_email(self):
        data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password': 'TestPass123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123',
            role='user'
        )

    def test_user_login_success(self):
        data = {
            'username': 'testuser',
            'password': 'TestPass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn('access', response_data['data'])
        self.assertIn('refresh', response_data['data'])
        self.assertIn('user', response_data['data'])
        self.assertEqual(response_data['data']['user']['username'], 'testuser')
        self.assertEqual(response_data['data']['user']['role'], 'user')

    def test_user_login_wrong_password(self):
        data = {
            'username': 'testuser',
            'password': 'WrongPassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_nonexistent_user(self):
        data = {
            'username': 'nonexistent',
            'password': 'TestPass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_missing_username(self):
        data = {
            'password': 'TestPass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_missing_password(self):
        data = {
            'username': 'testuser'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TokenRefreshTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.refresh_url = reverse('token_refresh')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123'
        )

    def test_token_refresh_success(self):
        login_data = {
            'username': 'testuser',
            'password': 'TestPass123'
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        refresh_token = login_response.json()['data']['refresh']

        refresh_data = {
            'refresh': refresh_token
        }
        response = self.client.post(self.refresh_url, refresh_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.json()['data'])

    def test_token_refresh_invalid_token(self):
        data = {
            'refresh': 'invalid.token.here'
        }
        response = self.client.post(self.refresh_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh_missing_token(self):
        response = self.client.post(self.refresh_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLogoutTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123'
        )

    def test_user_logout_success(self):

        login_data = {
            'username': 'testuser',
            'password': 'TestPass123'
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        tokens = login_response.json()['data']
        access_token = tokens['access']
        refresh_token = tokens['refresh']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        logout_data = {
            'refresh': refresh_token
        }
        response = self.client.post(self.logout_url, logout_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logout_without_authentication(self):
        data = {
            'refresh': 'some.refresh.token'
        }
        response = self.client.post(self.logout_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_logout_missing_refresh_token(self):
        login_data = {
            'username': 'testuser',
            'password': 'TestPass123'
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        access_token = login_response.json()['data']['access']

        # Try logout without refresh token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post(self.logout_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserModelTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, 'user')
        self.assertTrue(user.check_password('TestPass123'))

    def test_create_admin_user(self):
        user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='AdminPass123',
            role='admin'
        )
        self.assertEqual(user.role, 'admin')

    def test_user_string_representation(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPass123'
        )
        self.assertEqual(str(user), 'testuser (user)')

    def test_unique_email_constraint(self):
        User.objects.create_user(
            username='user1',
            email='test@example.com',
            password='TestPass123'
        )
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='user2',
                email='test@example.com',
                password='TestPass123'
            )

    def test_unique_username_constraint(self):
        User.objects.create_user(
            username='testuser',
            email='test1@example.com',
            password='TestPass123'
        )
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='testuser',
                email='test2@example.com',
                password='TestPass123'
            )
