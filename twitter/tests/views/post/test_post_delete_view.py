from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from twitter.models import Post

User = get_user_model()


class PostDeleteViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.owner = User.objects.create_user(
            username="owner", email="owner@example.com", password="test1234"
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@example.com", password="test1234"
        )

        self.post = Post.objects.create(
            author=self.owner, content="Post a ser deletado")
        self.url = reverse("post-delete", kwargs={"pk": self.post.pk})

    def test_owner_can_delete_post(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_non_owner_cannot_delete_post(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_delete_post(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_nonexistent_post_returns_404(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("post-delete", kwargs={"pk": 9999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
