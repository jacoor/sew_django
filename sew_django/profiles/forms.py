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
from django.contrib.auth.hashers import UNUSABLE_PASSWORD

from sew_django.profiles.models import Profile


def get_user_by_email(email):
    users = Profile.objects.all().only('email', 'id', 'is_active')
    for user in users:
        if user.email == email:
            return user


class EmailAuthenticationForm(AuthenticationForm):
    """
    Extends the standard django AuthenticationForm, to support 75 character
    usernames. 75 character usernames are needed to support the EmailOrUsername
    auth backend.
    """
    username = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': _('Password')}))

    def __init__(self, *args, **kwargs):
        super(EmailAuthenticationForm, self).__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = _("Your email or password is incorrect <br />"
                           "<a href='%s'>Forgot your password</a>") % reverse('password_reset')

'''
class PasswordResetForm(DjangoPasswordResetForm):
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.error_messages['unknown'] = mark_safe(_("There is no SenseHealth account registered with that email address. "
                           "<a href='%s'>Sign up with Sense Health</a>") % reverse('register'))

    def clean_email(self):
        """
        Validates that an active user exists with the given email address.
        """
        email = self.cleaned_data["email"]
        user = get_user_by_email(email)
        self.users_cache = [user]
        if not user:
            raise forms.ValidationError(self.error_messages['unknown'])
        if not any(user.is_active for user in self.users_cache):
            # none of the filtered users are active
            raise forms.ValidationError(self.error_messages['unknown'])
        if any((user.password == UNUSABLE_PASSWORD)
               for user in self.users_cache):
            raise forms.ValidationError(self.error_messages['unusable'])
        return email

    def save(self, domain_override=None,
             subject_template_name='emails/password_reset_subject.txt',
             email_template_name='emails_final/email_reset_password_content.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'STATIC_URL': settings.STATIC_URL,
                'user': user,
                'site': current_site,
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            email = EmailMessage(subject, email, from_email, [user.email])
            email.content_subtype = "html"
            email.send()


class ValidatingPasswordChangeForm(auth.forms.SetPasswordForm):
    MIN_LENGTH = 8

    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')

        # At least MIN_LENGTH long
        if len(password1) < self.MIN_LENGTH:
            raise forms.ValidationError("The new password must be at least %d characters long." % self.MIN_LENGTH)

        # At least one letter and one non-letter
        first_isalpha = password1[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password1):
            raise forms.ValidationError("The new password must contain at least one letter and at least one digit or"
                                        " punctuation character.")

        # ... any other validation you want ...

        return password1
'''
