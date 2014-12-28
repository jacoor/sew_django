# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sew_django.profiles.utils.sizeChecker


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='accept_of_sending_data_to_WOSP',
            field=models.BooleanField(default=False, verbose_name='Wyra\u017cam zgod\u0119 na przekazanie moich danych do fundacji Wielka Orkiestra \u015awi\u0105tecznej Pomocy z siedzib\u0105 w Warszawie przy ul. Dominika\u0144ska 19c gdzie dane b\u0119d\u0105 przetwarzane stosownie do postanowie\u0144 Ustawy z dnia 29 sierpnia 1997 r. o ochronie danych osobowych (Dz. U. nr 133, poz. 883 ze zm.) w celu organizacji Fina\u0142u Wielkiej Orkiestry \u015awi\u0105tecznej Pomocy. Przyjmuj\u0119 do wiadomo\u015bci \u017ce wyra\u017cenie niniejszej zgody jest wymagane w celu kontynuowania rejestracji.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='consent_processing_of_personal_data',
            field=models.BooleanField(default=False, verbose_name='Wyra\u017cam zgod\u0119 na przetwarzanie podanych danych osobowych przez Stowarzyszenie Hobbyst\xf3w Kolejowych z siedzib\u0105 w Warszawie przy ul. Orl\u0105t Lwowskich 38, stosownie do postanowie\u0144 Ustawy z dnia 29 sierpnia 1997 r. o ochronie danych osobowych (Dz. U. nr 133, poz. 883 ze zm.) w celu organizacji 23 Fina\u0142u Wielkiej Orkiestry \u015awi\u0105tecznej Pomocy we Wroc\u0142awiu. O\u015bwiadczam, \u017ce zosta\u0142em poinformowany, \u017ce podanie moich danych osobowych ma charakter dobrowolny oraz, \u017ce przys\u0142uguje mi prawo wgl\u0105du do nich, jak r\xf3wnie\u017c mo\u017cliwo\u015b\u0107 ich poprawiania. Przyjmuj\u0119 do wiadomo\u015bci \u017ce wyra\u017cenie niniejszej zgody jest wymagane w celu kontynuowania rejestracji.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=sew_django.profiles.utils.sizeChecker.ContentTypeRestrictedFileField(help_text='Zdj\u0119cie na identyfikator. Ma to by\u0107 zdj\u0119cie twarzy, bez ciemnych okular\xf3w, masek itp. Maksymalny rozmiar pliku 2MB. Preferowane zdj\u0119cie o rozmiarze 800x800px - inne b\u0119d\u0105 przeskalowane automatycznie, co mo\u017ce powodowa\u0107 nieoczekiwane skutki. Je\u015bli wy\u015blesz nam niepoprawne zdj\u0119cie mo\u017cesz zosta\u0107 wykluczony z procesu rekrutacji.', upload_to=b'photos', null=True, verbose_name='zdj\u0119cie', blank=True),
            preserve_default=True,
        ),
    ]
