from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from ...models import User


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'followers_count', 'following_count']

    @extend_schema_field(serializers.IntegerField())
    def get_followers_count(self, obj) -> int:
        return obj.followers.count()

    @extend_schema_field(serializers.IntegerField())
    def get_following_count(self, obj) -> int:
        return obj.following.count()
