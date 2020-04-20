from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Lista de cohortes de Academlo

    COURSE_START = [
        ('J2019', 'Julio 2019'),
        ('E2020', 'Enero 2020'),
        ('M2020', 'Mayo 2020'),
    ]

    GENDER = [
        ('M', 'Hombre'),
        ('F', 'Mujer')
    ]

    # Campos de usuario
    first_name = models.CharField(max_length=200, blank=False)
    last_name = models.CharField(max_length=200, blank=False)
    username = models.CharField(max_length=200, blank=False, unique=True)
    email = models.EmailField(unique=True, max_length=300, blank=False)
    course = models.CharField(choices=COURSE_START, max_length=5)
    gender = models.CharField(choices=GENDER, max_length=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        return self.username
