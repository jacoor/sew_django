# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from localflavor.pl.forms import PLPESELField
# Create your models here.

class ProfileManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = ProfileManager.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

    def get_by_email(self, username):
        return self.get(**{'email': username})

    def get_by_pesel(self, username):
        return self.get(**{'pesel': username})

class Profile(AbstractBaseUser, PermissionsMixin):
    PeselValidators = ()
    username = models.CharField(u'nazwa użytkownika', max_length=100, unique=True)
    email = models.EmailField('adres email', max_length=110, db_index=True, unique=True)
    first_name = models.CharField(u'imię', max_length=100, blank=True)
    last_name = models.CharField('nazwisko', max_length=30, blank=True)
    date_joined = models.DateTimeField('data rejestracji', auto_now_add=True)
    pesel = models.CharField('PESEL', unique=True, max_length=11, db_index=True)

    token = models.CharField(max_length=40, blank=True)

    USERNAME_FIELD = 'username'

    objects = ProfileManager()
    
    is_staff = models.BooleanField('staff status', default=False,
        help_text='Designates whether the user can log into this admin '
                    'site.')
    is_active = models.BooleanField('active', default=True,
        help_text='Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.last_name

    def get_username(self):
        return self.username
