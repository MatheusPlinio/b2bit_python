from rest_framework import serializers


class FeedAuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()


class FeedPostSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    author = FeedAuthorSerializer()
    content = serializers.CharField()
    created_at = serializers.DateTimeField()
    likes_count = serializers.IntegerField()
    is_liked = serializers.BooleanField()
