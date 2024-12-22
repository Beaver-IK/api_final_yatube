from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Follow(models.Model):
    """Промежуточная модель для реализации подписок (многие ко многим)
    между пользователями.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Пользователь',
        null=False, blank=False
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписан на',
        null=False, blank=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            )
        ]

    def __str__(self):
        return f"{self.user} подписан на {self.following}"


class Post(models.Model):
    """Модель публикаций пользователей."""

    text = models.TextField(null=False, blank=False)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE,
        null=True, blank=True, related_name='groups')

    def __str__(self):
        return self.text
    
    class Meta:
        ordering = ['-pub_date', 'author']


class Comment(models.Model):
    """Модель комментариев пользователей."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(null=False, blank=False)
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
