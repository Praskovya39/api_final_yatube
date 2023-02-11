from django.db import models
from django.contrib.auth import get_user_model
from yatube_api.settings import NUM_OF_LETTERS

User = get_user_model()


class Post(models.Model):
    text = models.TextField(
        verbose_name='Содержание поста',
        help_text='Напишите текст поста')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='По умолчанию текущая дата')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор поста',
        help_text='Кто написал и опубликовал пост')
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, в которую определен пост (необязательно)')
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:NUM_OF_LETTERS]


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название группы',
        help_text='Как называется группа')
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг',
        help_text='имы в адресной строке')
    description = models.TextField(
        verbose_name='Описание группы',
        help_text='Основна сфера группы')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
        help_text='Что комментируем')
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='По умолчанию текущая дата')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор коммента',
        help_text='Комментирующий')
    text = models.TextField(
        verbose_name='Содержание комментария',
        help_text='Напишите текст комментария')

    def __str__(self):
        return self.text[:NUM_OF_LETTERS]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Тот, кто подписывается')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Кумир',
        help_text='На кого подписываются')

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'user'), name='unique_following'
            ),
        )

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
