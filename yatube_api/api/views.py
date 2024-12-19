from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import ListCreateAPIView

from posts.models import Group, Post, Follow
from api.permissions import IsOwnerOrReadOnly
from api.serializers import (CommentSerializer, GroupSerializer,
                             PostSerializer, FollowSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для API постов."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для API сообществ."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для API комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_post(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return post

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer):
        serializer.save(post=self.get_post(), author=self.request.user)


class FollowApiView(ListCreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        return 
        

