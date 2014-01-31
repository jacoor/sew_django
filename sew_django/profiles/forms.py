# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm, \
    AdminPasswordChangeForm as DjagnoAdminPasswordChangeForm, UserCreationForm, \
    AuthenticationForm as DjangoAuthenticationForm

from django.utils.translation import ugettext_lazy as _
from passwords.fields import PasswordField

from sew_django.profiles.models import Profile

class ValidatingSetPasswordForm(SetPasswordForm):
    new_password1 = PasswordField(label=_("New password"))
    new_password2 = PasswordField(label=_("New password confirmation"))
 
class ValidatingPasswordChangeForm(PasswordChangeForm):
    new_password1 = PasswordField(label=_("New password"))
    new_password2 = PasswordField(label=_("New password confirmation"))

class AdminPasswordChangeForm(DjagnoAdminPasswordChangeForm):
    password1 = PasswordField(label=_("New password"))
    password2 = PasswordField(label=_("New password confirmation"))

class UserAdminCreationForm(UserCreationForm):
    password1 = PasswordField(label=_("New password"))
    password2 = PasswordField(label=_("New password confirmation"))

class AuthenticationForm(DjangoAuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = _(u"Numer PESEL lub adres email")
        self.error_messages['invalid_login'] = _(u"Wprowadź poprawny numer PESEL lub adres email.")

class PeselForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['pesel',]

class RegisterUserFullForm(forms.ModelForm):

    password = PasswordField(label=_("New password"))
    password_confirm = PasswordField(label=_("New password confirmation"))

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError(_("Passwords doesn't match."))
        return password_confirm
    
    class Meta:
        model = Profile
        fields = ['pesel','email', 'photo', 'first_name', 'last_name', 'street', 'house', 'flat', 'zip', 'city', 'phone',
            'workplace_name', 'workplace_address', 'workplace_zip', 'workplace_city', 'password','password_confirm']
