from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from api.permissions import IsOwnerOrReadOnly
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from posts.models import Group, Post


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


class FollowListCreateViewSet(ListModelMixin, CreateModelMixin,
                              viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.following.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
