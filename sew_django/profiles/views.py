# -*- coding: utf-8 -*-
import urlparse
from django.shortcuts import render
from django.views.generic import TemplateView, RedirectView, CreateView
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from sew_django.profiles.forms import AuthenticationForm, PeselForm

from sew_django.profiles.models import Profile
#from sew_django.emails.send import send_email


class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        response = super(LogoutView, self).get(request, *args, **kwargs)
        return response


class IndexView(TemplateView):
    template_name = 'index.html'
    login_prefix = 'login'
    pesel_prefix = 'pesel'

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context['login_form'] = AuthenticationForm(prefix=self.login_prefix)
        context['pesel_form'] = PeselForm(prefix=self.pesel_prefix)
        return context

class LoginView(IndexView):
    template_name = 'login.html'
    redirect_field_name = 'next'

    def get_context_data(self, *args, **kwargs):
        context = super(LoginView, self).get_context_data(*args, **kwargs)
        redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')
        context[self.redirect_field_name] = redirect_to
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
            login_form = AuthenticationForm(
                prefix=self.login_prefix,
                data=request.POST,
            )
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
                if user.is_staff and redirect_to == settings.LOGIN_REDIRECT_URL:
                    response = HttpResponseRedirect(settings.ADMIN_LOGIN_REDIRECT_URL)
                else:
                    response = HttpResponseRedirect(redirect_to)
                return response
            context['login_form'] = login_form

        self.request.session.set_test_cookie()
        return self.render_to_response(context)

class RegisterView(IndexView):
    template_name = "register/form.html"

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)

        if request.method == "POST":
            pesel_form = PeselForm(
                prefix=self.pesel_prefix,
                data=request.POST,
            )
            if pesel_form.is_valid():
                response = HttpResponseRedirect("%s?pesel=%s" % (reverse('register-full'), pesel_form.cleaned_data['pesel']))
                return response
            context['pesel_form'] = pesel_form

        return self.render_to_response(context)

class RegisterViewFull(CreateView):
    template_name = "register/full.html"
    model = Profile
    fields = ['pesel','email', 'photo', 'first_name', 'last_name', 'street', 'house', 'flat', 'zip', 'city', 'phone',
        'workplace_name', 'workplace_address', 'workplace_zip', 'workplace_city']


    def get(self, request, *args, **kwargs):
        if not request.GET.get('pesel'):
            return HttpResponseRedirect(reverse('register'))

        return super(RegisterViewFull, self).get(request, *args, **kwargs)

    def get_initial(self, *args, **kwargs):
        initial = super(RegisterViewFull, self).get_initial(*args, **kwargs)
        pesel = self.request.GET.get("pesel")
        initial['pesel'] = self.request.GET.get('pesel')
        return initial