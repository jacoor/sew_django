# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from sorl.thumbnail import ImageField

from sew_django.profiles.fields import PLPESELModelField, PLPostalCodeModelField

class ProfileManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError(_(u'The given email must be set'))
        email = ProfileManager.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_superuser=False,
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
    photo = ImageField(u'zdjęcie', upload_to='photos', null=True, blank=True, 
        help_text =u"Zdjęcie na identyfikator. Ma to być zdjęcie twarzy, bez ciemnych okularów, masek itp." 
        +u" Maksymalny rozmiar pliku 2 MB. Preferowane zdjęcie o rozmiarze 800x800px - inne będą" 
        +u" przeskalowane automatycznie, co może powodować nieoczekiwane skutki. Jeśli wyślesz nam niepoprawne zdjęcie" 
        +u" możesz zostać wykluczony z procesu rekrutacji.") 
    pesel = PLPESELModelField('PESEL', unique=True, max_length=11, db_index=True, 
        error_messages = {'unique' : 'Numer PESEL już istnieje w naszej bazie. <a href="/login/">Zaloguj się</a>.'})
    username = models.CharField(u'nazwa użytkownika', max_length=100, unique=True)
    email = models.EmailField('adres email', max_length=255, db_index=True, unique=True)
    first_name = models.CharField(u'imię', max_length=100)
    last_name = models.CharField('nazwisko', max_length=100)
    date_joined = models.DateTimeField('data rejestracji', auto_now_add=True,)
    #miejsce zamieszkania
    street = models.CharField('ulica', max_length=255)
    house = models.CharField('numer domu', max_length=255)
    flat = models.CharField('numer mieszkania', max_length=10, blank=True, null=True)
    zip = PLPostalCodeModelField('kod pocztowy', max_length=6)
    city = models.CharField(u"miejscowość", max_length=255)
    phone = models.CharField(u"numer telefonu wraz z numerem kierunkowym", max_length=100)
    workplace_name = models.CharField(u"nazwa szkoły lub zakładu pracy", max_length=255, blank=True, null=True)
    workplace_address = models.CharField(u"adres uczelni lub zakładu pracy", max_length=255, blank=True, null=True)
    workplace_zip = PLPostalCodeModelField('kod pocztowy', max_length=6, blank=True, null=True)
    workplace_city = models.CharField(u"miejscowość", max_length=255, blank=True, null=True)
    consent_processing_of_personal_data = models.BooleanField(u"Wyrażam zgodę na przetwarzanie podanych danych"
        + u" osobowych przez Stowarzyszenie Hobbystów Kolejowych z siedzibą w Warszawie przy ul. Orląt Lwowskich 38,"
        + u" stosownie do postanowień Ustawy z dnia 29 sierpnia 1997 r. o ochronie danych osobowych" 
        + u" (Dz. U. nr 133, poz. 883 ze zm.) w celu organizacji XXX Finału Wielkiej Orkiestry Świątecznej Pomocy" 
        + u" we Wrocławiu. Oświadczam, że zostałem poinformowany, że podanie moich danych osobowych ma charakter "
        + u" dobrowolny oraz, że przysługuje mi prawo wglądu do nich, jak również możliwość ich poprawiania." 
        + u"Przyjmuję do wiadomości że wyrażenie niniejszej zgody jest wymagane w celu kontynuowania rejestracji.", 
        default = True)

    date_consent_processing_of_personal_data = models.DateTimeField(u'Data wyrażenia zgody na przetwarzanie danych',
        auto_now_add=True)

    accept_of_sending_data_to_WOSP = models.BooleanField(u"Wyrażam zgodę na przekazanie moich danych do fundacji"
        + u" Wielka Orkiestra Świątecznej Pomocy z siedzibą w Warszawie przy ul. Dominikańska 19c"
        + u" gdzie dane będą przetwarzane stosownie do postanowień Ustawy z dnia 29 sierpnia 1997 r." 
        + u" o ochronie danych osobowych (Dz. U. nr 133, poz. 883 ze zm.) w celu organizacji Finału Wielkiej"
        + u" Orkiestry Świątecznej Pomocy. Przyjmuję do wiadomości że wyrażenie niniejszej" 
        + u" zgody jest wymagane w celu kontynuowania rejestracji.", 
        default = True)
    date_accept_of_sending_data_to_WOSP = models.DateTimeField(u'Data wyrażenia zgody na przekazanie danych do WOŚP',
        auto_now_add=True)

    token = models.CharField(max_length=40, blank=True)

    read_only = models.BooleanField('edycja zablokowana', default = False, 
        help_text = "Dane użytkownika tylko do odczytu, zmiana możliwa jedynie przez super administratora")

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
