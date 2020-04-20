from django.db import models

from accounts.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(db_index=True, unique=True, max_length=255)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(blank=True, max_length=400)
    body = RichTextUploadingField()
    image = models.ImageField(upload_to='featured_image', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', 'title')

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(blank=False)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + self.author.username
