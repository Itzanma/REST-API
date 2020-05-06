from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import Event

@receiver(pre_save, sender=Event)
def add_slug_to_event_if_not_exist(sender, instance, *args, **kwargs):
    MAXIMUM_SLUG_LENGTH = 255

    if instance and not instance.slug:
        slug = slugify(instance.title)

        if len(slug) > MAXIMUM_SLUG_LENGTH:
            slug = slug[:MAXIMUM_SLUG_LENGTH]

        while len(slug) > MAXIMUM_SLUG_LENGTH:
            parts = slug.split('-')

            if len(parts) is 1:
                slug = slug[:MAXIMUM_SLUG_LENGTH  - 1]
            else:
                slug = '-'.join(parts[:-1])

        instance.slug = slug