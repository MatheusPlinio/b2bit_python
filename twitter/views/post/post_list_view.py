from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from twitter.models import Post
from twitter.serializers.post.post_serializer import PostSerializer
from twitter.permissions import IsOwnerOrReadOnly


@extend_schema(tags=["Post"])
class PostListView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        queryset = Post.objects.select_related(
            'author').all().order_by('-created_at')
        if user_id:
            queryset = queryset.filter(author_id=user_id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
