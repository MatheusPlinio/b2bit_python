from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core.cache import cache
from twitter.models import Post
from twitter.serializers.post.post_serializer import PostSerializer

User = get_user_model()


class UserFeedViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            email="test@example.com",
            password="1234"
        )
        self.client.force_authenticate(user=self.user)

        self.author = User.objects.create_user(
            username="daniel",
            email="daniel@example.com",
            password="abcd"
        )
        self.post = Post.objects.create(
            author=self.author, content="Teste de postagem")

    def test_user_feed_returns_cached_data(self):
        expected_data = PostSerializer(
            [self.post],
            many=True,
            context={"request": None}
        ).data

        cache.set(f"user_feed_{self.user.id}", expected_data, timeout=3600)

        response = self.client.get("/api/user/feed/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_data)
