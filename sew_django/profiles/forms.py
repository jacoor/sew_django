# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm, \
    AdminPasswordChangeForm as DjagnoAdminPasswordChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from passwords.fields import PasswordField

from sew_django.profiles.models import Profile

class BaseValidatingForm(forms.Form):
    new_password1 = PasswordField(label=_("New password"))
    new_password2 = PasswordField(label=_("New password confirmation"))

class ValidatingSetPasswordForm(SetPasswordForm):
    new_password1 = PasswordField(label=_("New password"))
    new_password2 = PasswordField(label=_("New password confirmation"))
 
class ValidatingPasswordChangeForm(PasswordChangeForm):
    new_password1 = PasswordField(label=_("New password"))
    new_password2 = PasswordField(label=_("New password confirmation"))

class AdminPasswordChangeForm(DjagnoAdminPasswordChangeForm):
    new_password1 = PasswordField(label=_("New password"))
    new_password2 = PasswordField(label=_("New password confirmation"))

class UserAdminCreationForm(forms.ModelForm):
    password1 = PasswordField(label=_("New password"))
    password2 = PasswordField(label=_("New password confirmation"))

    class Meta:
        model = Profile
        fields = ("email",)

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user