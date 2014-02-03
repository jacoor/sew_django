# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail.admin import AdminImageMixin

from sew_django.profiles.models import Profile
from sew_django.profiles.forms import UserAdminCreationForm, AdminPasswordChangeForm

#uses sorl.thumbnail for admin as described here: from sorl.thumbnail import ImageField
class UserAdmin(AdminImageMixin, UserAdmin):
    list_display = ('email', 'is_staff')
    ordering = ('email',)
    readonly_fields=('date_joined','consent_processing_of_personal_data',
        'date_consent_processing_of_personal_data', 'accept_of_sending_data_to_WOSP',
        'date_accept_of_sending_data_to_WOSP',)
    fieldsets = ()
    add_form = UserAdminCreationForm
    change_password_form = AdminPasswordChangeForm

admin.site.register(Profile, UserAdmin)