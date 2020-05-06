from django.db import models

from accounts.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(db_index=True, unique=True, max_length=255)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(blank=True, max_length=400)
    # El campo RichTextUploading lo heredo de CKEDITOR
    body = RichTextUploadingField()
    image = models.ImageField(upload_to='featured_image', blank=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

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
