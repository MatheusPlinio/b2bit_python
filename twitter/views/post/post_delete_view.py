from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from twitter.models import Post
from twitter.serializers.post.post_serializer import PostSerializer
from twitter.permissions import IsOwnerOrReadOnly


@extend_schema(tags=["Post"])
class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
