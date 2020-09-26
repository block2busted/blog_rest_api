from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models

from articles.models import Article

User = get_user_model()


class CommentManager(models.Manager):
    def parent_only(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        qs = super(CommentManager, self).filter(article=instance).filter(parent=None)
        return qs

    def create_by_model_type(self, model_type, slug, content, user, parent_obj=None):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            some_model = model_qs.first().model_class()
            obj_qs = some_model.objects.filter(slug=slug)
            if obj_qs.exists() and obj_qs.count() == 1:
                instance = self.model()
                instance.content = content
                instance.author = user
                instance.content_type = model_qs.first()
                instance.article_id = obj_qs.first().id
                if parent_obj:
                    instance.parent = parent_obj
                instance.save()
                return instance
        return None


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, help_text='Article')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text='Author')
    content = models.TextField(help_text='Content', max_length=256)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, help_text='Parent')
    created = models.DateTimeField(auto_now_add=True, help_text='Created')
    updated = models.DateTimeField(auto_now=True, help_text='Updated')

    objects = CommentManager()

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
        if self.parent is not None:
            return False
        return True