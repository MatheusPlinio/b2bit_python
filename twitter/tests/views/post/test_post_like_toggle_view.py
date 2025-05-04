from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from twitter.models import Post, Follow
from django.core.cache import cache
from django.contrib.auth import get_user_model

User = get_user_model()


class PostLikeToggleViewTestCase(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username="author", password="test123", email="author@example.com")
        self.follower = User.objects.create_user(
            username="follower", password="test123", email="follower@example.com")
        Follow.objects.create(follower=self.follower, following=self.author)

        self.post = Post.objects.create(
            author=self.author, content="Test post")
        self.url = reverse("post-like", kwargs={"pk": self.post.id})
        self.client.force_authenticate(user=self.follower)

    @patch("twitter.views.post.post_like_toggle_view.update_post_likes_count.delay")
    def test_user_can_like_post(self, mock_task):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.follower, self.post.likes.all())
        mock_task.assert_called_once_with(self.post.id)

    @patch("twitter.views.post.post_like_toggle_view.update_post_likes_count.delay")
    def test_user_can_unlike_post(self, mock_task):
        self.post.likes.add(self.follower)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.follower, self.post.likes.all())
        mock_task.assert_called_once_with(self.post.id)

    @patch("twitter.views.post.post_like_toggle_view.update_post_likes_count.delay")
    def test_feed_cache_is_cleared_for_related_users(self, mock_task):
        user_ids = [self.follower.id, self.author.id]
        for uid in user_ids:
            cache.set(f"user_feed_{uid}", "cached_data")

        self.client.post(self.url)

        for uid in user_ids:
            self.assertIsNone(cache.get(f"user_feed_{uid}"))
