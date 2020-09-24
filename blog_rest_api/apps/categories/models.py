from django.db import models
from pytils.translit import slugify
from PIL import Image


class Category(models.Model):
    title = models.CharField(max_length=32, help_text='Title')
    description = models.TextField(help_text='Description')
    image = models.ImageField(upload_to='categories/images', blank=True, null=True, help_text='Image')
    slug = models.SlugField(unique=True, max_length=100, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('title', )

    def __str__(self):
        return 'Category {}'.format(self.title)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)
        photo = Image.open(self.image.path)
        if photo.height > 300 or photo.width > 300:
            output_size = (300, 300)
            photo.thumbnail(output_size)
            photo.save(self.image.path)