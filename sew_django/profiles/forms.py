# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, \
    UserCreationForm
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from django.core.mail import EmailMessage
from django.template import loader
from django.utils.http import int_to_base36
from django.contrib import auth

from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.utils.translation import ugettext_lazy as _
from passwords.fields import PasswordField

from sew_django.profiles.models import Profile


def get_user_by_email(email):
    users = Profile.objects.all().only('email', 'id', 'is_active')
    for user in users:
        if user.email == email:
            return user
 
class ValidatingSetPasswordForm(SetPasswordForm):
    new_password2 = PasswordField(label=_("New password confirmation"))
 
class ValidatingPasswordChangeForm(PasswordChangeForm):
    new_password2 = PasswordField(label=_("New password confirmation"))