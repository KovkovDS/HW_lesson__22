from django.db import models


class BlogArticle(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок', unique=True)
    content = models.TextField(default='Здесь пока ничего нет.', verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog/images', null=True, blank=True, verbose_name='Превью')
    create_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    published = models.BooleanField(default=True, verbose_name='Опубликована')
    number_views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        if self.published:
            article_published = 'Да'
        else:
            article_published = 'Нет'
        return (f'\n\nЗаголовок: {self.title}.\nСоздана: {self.create_at}.\nОпубликована: {article_published}.'
                f'\nКоличество просмотров: {self.number_views}.')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['create_at']
