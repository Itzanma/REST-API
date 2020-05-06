from django.db import models


# Create your models here.


class Speaker(models.Model):
    name = models.CharField(max_length=400, blank=False)
    bio = models.TextField()

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=400, blank=False, unique=True)
    description = models.TextField(blank=False)
    speakers = models.ManyToManyField(Speaker)
    slug = models.SlugField(db_index=True, unique=True, max_length=255)
    image = models.ImageField(upload_to='event_image', blank=True)
    link = models.URLField(blank=True)
    day = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title

