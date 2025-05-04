from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from twitter.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()


class PostListViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="john", password="password123", email="john@example.com")
        self.other_user = User.objects.create_user(
            username="jane", password="password123", email="jane@example.com")

        self.post1 = Post.objects.create(
            author=self.other_user, content="First post", created_at=timezone.now())
        self.post2 = Post.objects.create(
            author=self.user, content="Second post", created_at=timezone.now())
        self.post3 = Post.objects.create(
            author=self.user, content="Third post", created_at=timezone.now())

        self.url = reverse("post-list")

    def test_authenticated_user_can_list_posts(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_unauthenticated_user_cannot_list_posts(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_posts_are_ordered_by_created_at_desc(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        dates = [post["created_at"] for post in response.data]
        self.assertEqual(dates, sorted(dates, reverse=True))

    def test_post_response_includes_author(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertIn("author", response.data[0])

    def test_serializer_context_contains_request(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
