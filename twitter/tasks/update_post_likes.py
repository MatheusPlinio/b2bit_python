from celery import shared_task
from django.core.cache import cache
from twitter.models import Post


@shared_task
def update_post_likes_count(post_id):
    try:
        post = Post.objects.get(id=post_id)
        likes_count = post.likes.count()
        cache.set(f"post_likes_count_{post_id}", likes_count, timeout=2 * 2)
        print(f"Contagem de likes do post {post_id} atualizada: {likes_count}")
    except Post.DoesNotExist:
        print(f"Post {post_id} não encontrado para atualizar likes.")
