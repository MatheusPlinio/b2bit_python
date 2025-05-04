from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema
from django.core.cache import cache
from ...models import Post
from ...serializers.post.post_serializer import PostSerializer
from twitter.tasks.invalidated_feed_cache import invalidate_followers_feed_cache_task
from twitter.serializers.post.responses.post_create_response_serializer import PostCreateResponseSerializer


@extend_schema(tags=["Post"], responses=({201: PostCreateResponseSerializer}))
class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        invalidate_followers_feed_cache_task(self.request.user.id)
        followers_ids = self.request.user.followers.values_list(
            'id', flat=True)
        for follower_id in followers_ids:
            cache.delete(f"user_feed_{follower_id}")
