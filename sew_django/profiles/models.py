from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.

class Profile(AbstractBaseUser):
    email = models.EmailField('adres email', max_length=110, unique=True)
    names = models.CharField('imiona', max_length=100, blank=True)
    last_name = models.CharField('nazwisko', max_length=30, blank=True)
    date_joined = models.DateTimeField('data rejestracji', auto_now_add=True)

    token = models.CharField(max_length=40, blank=True)

    USERNAME_FIELD = 'email'
