from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from twitter.models import Follow

User = get_user_model()


class FollowToggleViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alice", password="test1234", email="alice@example.com")
        self.target_user = User.objects.create_user(
            username="bob", password="test1234", email="bob@example.com")
        self.url = reverse("follow-toggle", args=[self.target_user.id])
        self.client.force_authenticate(user=self.user)

    def test_user_can_follow_another_user(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "followed")
        self.assertTrue(Follow.objects.filter(
            follower=self.user, following=self.target_user).exists())

    def test_user_can_unfollow_after_following(self):
        # Primeiro segue
        self.client.post(self.url)
        self.assertTrue(Follow.objects.filter(
            follower=self.user, following=self.target_user).exists())

        # Depois desfaz
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "unfollowed")
        self.assertFalse(Follow.objects.filter(
            follower=self.user, following=self.target_user).exists())
