from django.shortcuts import render

# Create your views here.

# -*- coding: utf-8 -*-
import urlparse

from django.views.generic import TemplateView, RedirectView
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages


from sew_django.profiles.models import Profile
from sew_django.profiles.forms import EmailAuthenticationForm,
#from sew_django.emails.send import send_email


class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        response = super(LogoutView, self).get(request, *args, **kwargs)
        return response


class IndexView(TemplateView):
    redirect_field_name = 'next'
    template_name = 'index'
    login_prefix = 'login'
    auto_id = False  # removes labels

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')
        context[self.redirect_field_name] = redirect_to
        context['login_form'] = EmailAuthenticationForm(prefix=self.login_prefix, auto_id=self.auto_id)
        return context

    def check_redirect(self, context):
        redirect_to = context.get(self.redirect_field_name)
        if not redirect_to:
            return settings.LOGIN_REDIRECT_URL

        netloc = urlparse.urlparse(redirect_to)[1]
        if netloc and netloc != self.request.get_host():
            return settings.LOGIN_REDIRECT_URL

        return redirect_to

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)
        redirect_to = self.check_redirect(context)

        if request.method == "POST":
            login_form = EmailAuthenticationForm(
                prefix=self.login_prefix,
                data=request.POST,
                auto_id=self.auto_id
            )
            if login_form.is_valid():
                auth_login(request, login_form.get_user())
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                response = HttpResponseRedirect(redirect_to)
                return response
            context['login_form'] = login_form

        self.request.session.set_test_cookie()
        return self.render_to_response(context)