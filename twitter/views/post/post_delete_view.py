from rest_framework import generics, permissions
from twitter.models import Post
from twitter.serializers.post.post_serializer import PostSerializer
from twitter.permissions import IsOwnerOrReadOnly

class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]