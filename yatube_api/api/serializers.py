from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post."""

    author = SlugRelatedField(slug_field='username', read_only=True)
    group = SlugRelatedField(
        slug_field='id',
        queryset=Group.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Post
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор модели Group."""

    class Meta:
        model = Group
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'author', 'post', 'created',)


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор модели Follow."""

    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following',)
        read_only_fields = ('id', 'user', 'following', 'created_at',)

    def validate_following(self, value):
        request_user = self.context['request'].user
        if value == request_user:
            raise ValidationError('Нельзя подписаться на самого себя.')
        if Follow.objects.filter(user=request_user, following=value).exists():
            raise ValidationError('Вы уже подписаны на этого пользователя.')
        return value
