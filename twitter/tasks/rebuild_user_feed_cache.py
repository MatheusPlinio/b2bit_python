from celery import shared_task
from django.core.cache import cache
from ..models import Post, User
from ..serializers.post.post_serializer import PostSerializer


@shared_task
def rebuild_user_feed_cache(user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return

    following_ids = list(user.following.values_list('id', flat=True))
    cache_key = f"user_feed_{user_id}"

    if following_ids:
        posts_qs = Post.objects.filter(author_id__in=following_ids)
    else:
        posts_qs = Post.objects.exclude(author_id=user_id)

    posts_qs = posts_qs.order_by('-created_at')[:10]
    serialized = PostSerializer(posts_qs, many=True, context={'request': None}).data
    cache.set(cache_key, serialized, timeout=60 * 5)
