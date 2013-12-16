# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.views import password_reset, password_reset_done, \
    password_reset_confirm, password_reset_complete

from django.contrib.auth.decorators import login_required    
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView


from sew_django.profiles.views import IndexView, LogoutView

urlpatterns = patterns('',
    url(r"^$", IndexView.as_view(), name='index'),
    url(r"^logout/$", LogoutView.as_view(), name="logout"),
    url(r'^reset_password/$', password_reset,{'template_name': 'password/reset.html'}, name="password_reset"),
    url(r'^password_reset_done/$', password_reset_done, {'template_name' : 'password/reset_done.html'}, \
        name="password_reset_done"),
    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, \
        {'template_name': 'password/reset_confirm.html'},name="password_reset_confirm"),
    url(r'^reset_password_complete/$', password_reset_complete, {'template_name':'password/reset_complete.html'},\
        name="password_reset_complete"),

    #url(r'^reset_password/$', password_reset, {'template_name': 'profiles/resetPassword.html', 'subject_template_name': 'emails/resetPassword/subject.txt', 'email_template_name': 'emails_final/email_reset_password_content.html', 'password_reset_form': PasswordResetForm}, name="password_reset"),
    #url(r'^reset_password_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'template_name': 'profiles/resetPasswordConfirm.html', 'set_password_form': ValidatingPasswordChangeForm}, name="password_reset_confirm"),
    #url(r'^reset_password_done/$', password_reset_done, {'template_name': 'profiles/resetPasswordDone.html'}),
    #url(r'^reset_password_complete/$', password_reset_complete, {'template_name': 'profiles/resetPasswordComplete.html'}),
)
