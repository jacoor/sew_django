# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from sorl.thumbnail.admin import AdminImageMixin

from sew_django.profiles.models import Profile
from sew_django.profiles.forms import AdminPasswordChangeForm, AdminRegisterUserFullForm


class UserAdmin(AdminImageMixin, UserAdmin):
    list_display = ('email', 'is_staff')
    ordering = ('email',)
    readonly_fields = (
        'date_joined', 'birthdate', 'consent_processing_of_personal_data',
        'date_consent_processing_of_personal_data', 'accept_of_sending_data_to_WOSP',
        'date_accept_of_sending_data_to_WOSP',
    )
    fieldsets = ()
    add_form = AdminRegisterUserFullForm
    change_password_form = AdminPasswordChangeForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': AdminRegisterUserFullForm.Meta.fields,
        }),
    )

admin.site.register(Profile, UserAdmin)
