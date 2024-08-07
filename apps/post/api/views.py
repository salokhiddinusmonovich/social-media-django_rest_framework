
from rest_framework.generics import (CreateAPIView,
                                     UpdateAPIView,
                                     ListAPIView,
                                     RetrieveAPIView, DestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework import parsers
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.post.models import Post, Tag, LikedPost, Comment, LikedComment
from .serializers import (PostCreateSerializer,
                          PostUpdateSerializer,
                          PostListSerializer,
                          LikePostSerializer,
                          CommentCreateSerializer,
                          PostDetailSerializer, CommentListSerializer)
from .permissions import IsOwner


class PostCreateAPIView(CreateAPIView):
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = (parsers.MultiPartParser, parsers.FileUploadParser, parsers.JSONParser)

    def perform_create(self, serializer):
        # print(self.request.data)
        serializer.save(user=self.request.user)


post_create = PostCreateAPIView.as_view()


class PostUpdateAPIView(UpdateAPIView):
    serializer_class = PostUpdateSerializer
    queryset = Post.objects.all()
    permission_classes = [IsOwner]

    lookup_field = 'id'

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj


post_update = PostUpdateAPIView.as_view()


class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()


post_list = PostListAPIView.as_view()

class PostDetailAPIView(RetrieveAPIView):
    serializer_class = PostDetailSerializer
    queryset = Post.objects.all().prefetch_related('comments__children')

    lookup_field = 'id'


post_detail = PostDetailAPIView.as_view()

class LikePostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        post_id = request.data.get('id')
        post = Post.objects.get(id=post_id)
        like = LikedPost.objects.filter(post=post,
                                        user=request.user).first()
        if not like:
            LikedPost.objects.create(user=request.user, post=post)

            return Response({"message": "liked"})
        like.delete()
        return Response({"message": "disliked"})


liked_post = LikePostAPIView.as_view()


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsOwner]
    lookup_field = 'id'

post_delete = PostDeleteAPIView.as_view()


class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentCreateSerializer
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


comment_create = CommentCreateAPIView.as_view()

class LikeCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        comment_id = request.data.get('id')
        comment = Comment.objects.get(id=comment_id)
        like = LikedComment.objects.filter(comment=comment,
                                        user=request.user).first()
        if not like:
            LikedComment.objects.create(user=request.user, comment=comment)

            return Response({"message": "liked"})
        like.delete()
        return Response({"message": "disliked"})


liked_comment = LikeCommentAPIView.as_view()


class CommentDeleteAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsOwner]
    lookup_field = 'id'


comment_delete = CommentDeleteAPIView.as_view()


class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    queryset = Comment.objects.all()


comment_list = CommentListAPIView.as_view()
