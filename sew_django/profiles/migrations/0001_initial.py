# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import sorl.thumbnail.fields
import sew_django.profiles.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('photo', sorl.thumbnail.fields.ImageField(help_text='Zdj\u0119cie na identyfikator. Ma to by\u0107 zdj\u0119cie twarzy, bez ciemnych okular\xf3w, masek itp. Maksymalny rozmiar pliku 2 MB. Preferowane zdj\u0119cie o rozmiarze 800x800px - inne b\u0119d\u0105 przeskalowane automatycznie, co mo\u017ce powodowa\u0107 nieoczekiwane skutki. Je\u015bli wy\u015blesz nam niepoprawne zdj\u0119cie mo\u017cesz zosta\u0107 wykluczony z procesu rekrutacji.', upload_to=b'photos', null=True, verbose_name='zdj\u0119cie', blank=True)),
                ('pesel', sew_django.profiles.fields.PLPESELModelField(db_index=True, unique=True, max_length=11, verbose_name=b'PESEL', error_messages={b'unique': b'Numer PESEL ju\xc5\xbc istnieje w naszej bazie. <a href="/login/">Zaloguj si\xc4\x99</a>.'})),
                ('username', models.CharField(unique=True, max_length=100, verbose_name='nazwa u\u017cytkownika')),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'adres email', db_index=True)),
                ('first_name', models.CharField(max_length=100, verbose_name='imi\u0119')),
                ('last_name', models.CharField(max_length=100, verbose_name=b'nazwisko')),
                ('rank', models.CharField(blank=True, max_length=2, verbose_name='ocena', choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)])),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name=b'data rejestracji')),
                ('street', models.CharField(max_length=255, verbose_name=b'ulica')),
                ('house', models.CharField(max_length=255, verbose_name=b'numer domu')),
                ('flat', models.CharField(max_length=10, null=True, verbose_name=b'numer mieszkania', blank=True)),
                ('zip', sew_django.profiles.fields.PLPostalCodeModelField(max_length=6, verbose_name=b'kod pocztowy')),
                ('city', models.CharField(max_length=255, verbose_name='miejscowo\u015b\u0107')),
                ('phone', models.CharField(max_length=100, verbose_name='numer telefonu wraz z numerem kierunkowym')),
                ('workplace_name', models.CharField(max_length=255, null=True, verbose_name='nazwa szko\u0142y lub zak\u0142adu pracy', blank=True)),
                ('workplace_address', models.CharField(max_length=255, null=True, verbose_name='adres uczelni lub zak\u0142adu pracy', blank=True)),
                ('workplace_zip', sew_django.profiles.fields.PLPostalCodeModelField(max_length=6, null=True, verbose_name=b'kod pocztowy', blank=True)),
                ('workplace_city', models.CharField(max_length=255, null=True, verbose_name='miejscowo\u015b\u0107', blank=True)),
                ('consent_processing_of_personal_data', models.BooleanField(default=True, verbose_name='Wyra\u017cam zgod\u0119 na przetwarzanie podanych danych osobowych przez Stowarzyszenie Hobbyst\xf3w Kolejowych z siedzib\u0105 w Warszawie przy ul. Orl\u0105t Lwowskich 38, stosownie do postanowie\u0144 Ustawy z dnia 29 sierpnia 1997 r. o ochronie danych osobowych (Dz. U. nr 133, poz. 883 ze zm.) w celu organizacji 23 Fina\u0142u Wielkiej Orkiestry \u015awi\u0105tecznej Pomocy we Wroc\u0142awiu. O\u015bwiadczam, \u017ce zosta\u0142em poinformowany, \u017ce podanie moich danych osobowych ma charakter dobrowolny oraz, \u017ce przys\u0142uguje mi prawo wgl\u0105du do nich, jak r\xf3wnie\u017c mo\u017cliwo\u015b\u0107 ich poprawiania. Przyjmuj\u0119 do wiadomo\u015bci \u017ce wyra\u017cenie niniejszej zgody jest wymagane w celu kontynuowania rejestracji.')),
                ('date_consent_processing_of_personal_data', models.DateTimeField(auto_now_add=True, verbose_name='Data wyra\u017cenia zgody na przetwarzanie danych')),
                ('accept_of_sending_data_to_WOSP', models.BooleanField(default=True, verbose_name='Wyra\u017cam zgod\u0119 na przekazanie moich danych do fundacji Wielka Orkiestra \u015awi\u0105tecznej Pomocy z siedzib\u0105 w Warszawie przy ul. Dominika\u0144ska 19c gdzie dane b\u0119d\u0105 przetwarzane stosownie do postanowie\u0144 Ustawy z dnia 29 sierpnia 1997 r. o ochronie danych osobowych (Dz. U. nr 133, poz. 883 ze zm.) w celu organizacji Fina\u0142u Wielkiej Orkiestry \u015awi\u0105tecznej Pomocy. Przyjmuj\u0119 do wiadomo\u015bci \u017ce wyra\u017cenie niniejszej zgody jest wymagane w celu kontynuowania rejestracji.')),
                ('date_accept_of_sending_data_to_WOSP', models.DateTimeField(auto_now_add=True, verbose_name='Data wyra\u017cenia zgody na przekazanie danych do WO\u015aP')),
                ('token', models.CharField(max_length=40, blank=True)),
                ('read_only', models.BooleanField(default=False, help_text=b'Dane u\xc5\xbcytkownika tylko do odczytu, zmiana mo\xc5\xbcliwa jedynie przez super administratora', verbose_name=b'edycja zablokowana')),
                ('is_staff', models.BooleanField(default=False, help_text=b'Designates whether the user can log into this admin site.', verbose_name=b'staff status')),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name=b'active')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'u\u017cytkownik',
                'verbose_name_plural': 'u\u017cytkownicy',
            },
            bases=(models.Model,),
        ),
    ]
