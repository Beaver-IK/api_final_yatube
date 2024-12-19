from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Comment, Post, Group, Follow


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    group = SlugRelatedField(
        slug_field='id',
        queryset=Group.objects.all(),
        allow_null=True,
        required=False,
    )
    class Meta:
        fields = '__all__'
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор модели Group."""

    class Meta:
        model = Group
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('id', 'author', 'post', 'created',)


class FollowSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = '__all__'
        model = Follow
    
        
