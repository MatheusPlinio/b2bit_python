from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from twitter.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()


class PostUpdateViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="john", password="password123", email="john@example.com")
        self.other_user = User.objects.create_user(username="jane", password="password123", email="jane@example.com")

        self.own_post = Post.objects.create(author=self.user, content="Original content")
        self.other_post = Post.objects.create(author=self.other_user, content="Not yours")

        self.url = reverse("post-update", kwargs={"pk": self.own_post.pk})

    def test_authenticated_user_can_update_own_post(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, {"content": "Updated content"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.own_post.refresh_from_db()
        self.assertEqual(self.own_post.content, "Updated content")

    def test_user_cannot_update_post_of_others(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("post-update", kwargs={"pk": self.other_post.pk})
        response = self.client.put(url, {"content": "Trying to hack"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_update_post(self):
        response = self.client.put(self.url, {"content": "Unauthorized update"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_response_contains_updated_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.url, {"content": "Final update"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Final update")