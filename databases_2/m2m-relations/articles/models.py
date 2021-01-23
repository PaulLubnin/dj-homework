from django.db import models


class Scope(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название раздела')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение', )
    scopes = models.ManyToManyField(Scope, related_name='articles', through='ScopeSetter')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class ScopeSetter(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    scope = models.ForeignKey('Scope', on_delete=models.CASCADE)
    is_main = models.BooleanField(verbose_name='Основной раздел')

    class Meta:
        ordering = ['-is_main']

    def __str__(self):
        return f'Статья "{self.article}" с тегом "{self.scope}"'
