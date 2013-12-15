# -*- coding: utf-8 -*-
from django.test import TestCase, RequestFactory, SimpleTestCase
from django.core.urlresolvers import reverse
from django.test.client import Client

from sew_django.profiles.models import Profile
#from sew_django.profiles.views import Index



def setup_view(view, request, *args, **kwargs):
    """*args and **kwargs you could pass to ``reverse()``."""
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class ProfileTests(TestCase):

    def setUp(self):
        self.user = Profile.objects.create(names='Joe',
                                            email='joe@doe.com',
                                            is_active=False)
        self.user.set_password('dump-password')
        self.user.save()

    def test_index(self):
        #request = RequestFactory().get(reverse('index'))
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        #request = RequestFactory().get(reverse('index'))
        response = self.client.login(email='joe@doe.com', password='dump-password')
        self.assertEqual(response, False) 
        self.user.is_active = True
        self.user.save()
        response = self.client.login(email='joe@doe.com', password='dump-password')
        self.assertEqual(response, True)

    def test_login_form_view(self):
        response = self.client.post("/", {})
        self.assertFormError(response, 'login_form', 'password', 'To pole jest wymagane.')
        self.assertFormError(response, 'login_form', 'username', 'To pole jest wymagane.')

        response = self.client.post("/", {'login-username':'xxx'})
        self.assertFormError(response, 'login_form', 'password', 'To pole jest wymagane.')
        
        response = self.client.post("/", {'login-password':'xxx'})
        self.assertFormError(response, 'login_form', 'username', 'To pole jest wymagane.')

        response = self.client.post("/", {'login-password':'xxx','login-username':'xxx'})
        self.assertFormError(response, 'login_form', None, u'Wprowadź poprawną adres email oraz hasło. Uwaga: wielkość liter ma znaczenie.')

        response = self.client.post("/", {'login-password':'dump-password','login-username':'joe@doe.com'})
        self.assertFormError(response, 'login_form', None, 'To konto jest nieaktywne.')

        self.user.is_active = True
        self.user.is_superuser = True
        self.user.save()
        response = self.client.post("/", {'login-password':'dump-password','login-username':'joe@doe.com'})
        self.assertRedirects(response, '/admin/', status_code=302, target_status_code=200)

