from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from rest_framework.generics import UpdateAPIView
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import status
from twitter.models import Post
from twitter.serializers.post.post_serializer import PostSerializer
from twitter.serializers.post.responses.post_update_response_serializer import PostUpdateResponseSerializer


@extend_schema(tags=["Post"], responses=({201: PostUpdateResponseSerializer}))
class PostUpdateView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['put']

    def get_object(self):
        obj = super().get_object()
        if obj.author != self.request.user:
            raise PermissionDenied(
                {"message": "Você não tem permissão para editar este post."})
        return obj

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response({"message": "Post atualizado com sucesso."}, status=status.HTTP_201_CREATED)
