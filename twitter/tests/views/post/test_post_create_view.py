from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core.cache import cache
from django.contrib.auth import get_user_model
from twitter.models import Post, Follow

User = get_user_model()


class PostCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="john", email="john@example.com", password="test1234"
        )
        self.follower = User.objects.create_user(
            username="jane", email="jane@example.com", password="test1234"
        )
        Follow.objects.create(follower=self.follower, following=self.user)

        self.client.force_authenticate(user=self.user)
        self.url = reverse("post-create")

    def test_create_post_successfully(self):
        response = self.client.post(self.url, {"content": "Novo post"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author, self.user)

    def test_cache_is_invalidated_for_followers(self):
        cache_key = f"user_feed_{self.follower.id}"
        cache.set(cache_key, "fake_data", timeout=60 * 60)

        self.assertIsNotNone(cache.get(cache_key))

        self.client.post(self.url, {"content": "Post que limpa cache"})
        self.assertIsNone(cache.get(cache_key))

    def test_create_post_without_authentication(self):
        self.client.logout()
        response = self.client.post(self.url, {"content": "Teste sem login"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
