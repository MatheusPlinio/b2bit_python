from celery import shared_task
from django.core.cache import cache
from django.contrib.auth import get_user_model
from twitter.models import Post
from twitter.models import Follow
from twitter.serializers.post.post_serializer import PostSerializer

User = get_user_model()


@shared_task
def rebuild_user_feed_cache(user_id):
    try:
        user = User.objects.get(id=user_id)

        followed_user_ids = Follow.objects.filter(
            follower_id=user.id
        ).values_list('following_id', flat=True)

        followed_posts = Post.objects.filter(
            author_id__in=followed_user_ids
        ).order_by("-created_at")[:100]

        posts = list(followed_posts)

        if len(posts) < 100:
            excluded_ids = list(followed_user_ids) + [user.id]
            remaining_needed = 100 - len(posts)

            additional_posts = Post.objects.exclude(
                author_id__in=excluded_ids
            ).order_by("-created_at")[:remaining_needed]

            posts += list(additional_posts)

        serialized_posts = PostSerializer(posts, many=True).data

        cache.set(f"user_feed_{user.id}", serialized_posts, timeout=2 * 2)

        print(
            f"Feed do usuário {user.username} reconstruído e armazenado no cache com {len(posts)} posts.")

    except User.DoesNotExist:
        print(f"Usuário com id {user_id} não encontrado.")
