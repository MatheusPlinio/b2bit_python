from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from django.core.cache import cache
from ..user.public_user_serializer import PublicUserSerializer
from ...models import Post


class PostSerializer(serializers.ModelSerializer):
    author = PublicUserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'content',
                  'created_at', 'likes_count', 'is_liked']

    @extend_schema_field(serializers.IntegerField)
    def get_likes_count(self, obj: Post) -> int:
        cache_key = f"post_likes_count_{obj.id}"
        count = cache.get(cache_key)
        if count is None:
            count = obj.likes.count()
            cache.set(cache_key, count, timeout=60)
        return count

    @extend_schema_field(serializers.BooleanField)
    def get_is_liked(self, obj: Post) -> bool:
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False
