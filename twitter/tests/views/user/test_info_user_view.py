from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from twitter.models import Follow

User = get_user_model()


class UserInfoViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="viewer",
            email="viewer@example.com",
            password="1234"
        )
        self.target_user = User.objects.create_user(
            username="target",
            email="target@example.com",
            password="abcd"
        )
        self.client.force_authenticate(user=self.user)

    def test_user_info_when_not_following(self):
        response = self.client.get(f"/api/user/{self.target_user.id}/info/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.target_user.id)
        self.assertEqual(response.data["username"], self.target_user.username)
        self.assertFalse(response.data["is_following"])

    def test_user_info_when_following(self):
        Follow.objects.create(follower=self.user, following=self.target_user)

        response = self.client.get(f"/api/user/{self.target_user.id}/info/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["is_following"])
