from django.contrib.auth import get_user_model
from django.db import models

from articles.models import Article

User = get_user_model()


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, help_text='Article')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text='Author')
    content = models.TextField(help_text='Content', max_length=256)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, help_text='Parent')
    created = models.DateTimeField(auto_now_add=True, help_text='Created')
    updated = models.DateTimeField(auto_now=True, help_text='Updated')

    def __str__(self):
        return 'Comment for article {}: {}'.format(self.article.title[:10], self.content[:16])

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('created', )

    def get_children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is None:
            return False
        return True