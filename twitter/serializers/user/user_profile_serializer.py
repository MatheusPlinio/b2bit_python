from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(
        source='followers.count', read_only=True)
    following_count = serializers.IntegerField(
        source='following.count', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'followers_count', 'following_count']
