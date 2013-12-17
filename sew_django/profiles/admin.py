# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from sew_django.profiles.models import Profile
from sew_django.profiles.forms import UserAdminCreationForm, AdminPasswordChangeForm


class UserAdmin(UserAdmin):
    list_display = ('email', 'is_staff')
    ordering = ('email',)
    readonly_fields=('date_joined',)
    fieldsets = ()
    add_form = UserAdminCreationForm
    change_password_form = AdminPasswordChangeForm

admin.site.register(Profile, UserAdmin)