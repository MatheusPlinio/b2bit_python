from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterViewTestCase(APITestCase):
    def setUp(self):

        self.url = reverse('register_user')
        self.valid_payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "strongpassword123"
        }

    def test_register_user_successfully(self):
        response = self.client.post(
            self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'],
                         self.valid_payload['username'])
        self.assertEqual(response.data['email'], self.valid_payload['email'])
        self.assertTrue(User.objects.filter(
            email=self.valid_payload['email']).exists())

    def test_register_user_missing_fields(self):
        invalid_payload = {
            "username": "",
            "email": "",
            "password": ""
        }
        response = self.client.post(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertIn('password', response.data)
