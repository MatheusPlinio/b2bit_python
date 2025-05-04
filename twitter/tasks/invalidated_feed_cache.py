from celery import shared_task
from django.core.cache import cache
from twitter.models import Follow


@shared_task
def invalidate_followers_feed_cache_task(user_id):
    follower_ids = Follow.objects.filter(
        following_id=user_id
    ).values_list("follower_id", flat=True)

    for follower_id in follower_ids:
        cache.delete(f"user_feed_{follower_id}")
