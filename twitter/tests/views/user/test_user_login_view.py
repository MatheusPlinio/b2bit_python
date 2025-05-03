from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()


class UserLoginViewTestCase(APITestCase):

    def setUp(self):
        self.username = "testuser"
        self.email = "testuser@example.com"
        self.password = "strong-password"
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )
        self.login_url = reverse('token_obtain_pair')

    def test_obtain_token_pair_success(self):

        data = {
            'email': self.email,
            'password': self.password
        }
        response = self.client.post(self.login_url, data, format='json')

        self.assertEqual(response.status_code, 200)

        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        self.assertIn('user', response.data)
        user_data = response.data['user']
        self.assertEqual(user_data['id'], self.user.id)
        self.assertEqual(user_data['email'], self.email)
        self.assertEqual(user_data['username'], self.username)

    def test_obtain_token_pair_failure(self):
        data = {
            'email': self.email,
            'password': 'wrong-password'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('detail', response.data)
        self.assertEqual(
            response.data['detail'], 'No active account found with the given credentials')
