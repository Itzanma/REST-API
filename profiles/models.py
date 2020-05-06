from django.db import models
from accounts.models import User


# Create your models here.

class Profile(models.Model):
    # Lista de interes favorito
    INTEREST = [
        ('FRONT', 'Frontend'),
        ('BACK', 'Backend'),
        ('FULL', 'Fullstack')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='profile_image', blank=True)
    interest = models.CharField(choices=INTEREST, max_length=10)

    def __str__(self):
        return self.user.username

