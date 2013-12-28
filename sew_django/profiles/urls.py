# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.views import password_reset, password_reset_done, \
    password_reset_confirm, password_reset_complete

from django.contrib.auth.decorators import login_required    
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from sew_django.profiles.views import IndexView, LogoutView, LoginView, PeselView
from sew_django.profiles.forms import ValidatingSetPasswordForm

urlpatterns = patterns('',
    url(r"^$", IndexView.as_view(), name='index'),
    url(r"^login/$", LoginView.as_view(), name='login'),
    url(r"^logout/$", LogoutView.as_view(), name="logout"),
    url(r"^pesel/$", PeselView.as_view(), name='pesel'),
    url(r'^reset_password/$', password_reset,{'template_name': 'password/reset.html'}, name="password_reset"),
    url(r'^password_reset_done/$', password_reset_done, {'template_name' : 'password/reset_done.html'}, \
        name="password_reset_done"),
    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, \
        {'template_name': 'password/reset_confirm.html', 'set_password_form' : ValidatingSetPasswordForm},name="password_reset_confirm"),
    url(r'^reset_password_complete/$', password_reset_complete, {'template_name':'password/reset_complete.html'},\
        name="password_reset_complete"),
)
