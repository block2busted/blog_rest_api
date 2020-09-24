from django.contrib.auth import get_user_model
from django.db import models
from pytils.translit import slugify

from categories.models import Category

User = get_user_model()


class Article(models.Model):
    title = models.CharField(max_length=64, help_text='Title')
    content = models.TextField(help_text='Content')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, help_text='Category')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, help_text='Author')
    created = models.DateTimeField(auto_now_add=True, help_text='Created datetime')
    updated = models.DateTimeField(auto_now=True, help_text='Updated datetime')
    views_count = models.IntegerField(default=0, help_text='Views count')
    slug = models.SlugField(unique=True, blank=True, null=True, help_text='Slug')
    is_active = models.BooleanField(default=False, help_text='Is active')

    def __str__(self):
        return 'Article {}'.format(self.title)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ('created',)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)
