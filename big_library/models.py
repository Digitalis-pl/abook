from django.db import models

# Create your models here.


class Document(models.Model):
    title = models.CharField(max_length=200,  verbose_name='Заголовок')
    content = models.TextField(verbose_name='Текст')
    file = models.URLField(blank=True, null=True, verbose_name='Ссылка на контент')
    created_at = models.DateTimeField(auto_now_add=True,  verbose_name='Дата загрузки')

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'

    def __str__(self):
        return self.title
