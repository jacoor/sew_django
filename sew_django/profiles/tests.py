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
        self.assertTemplateUsed(response, 'index.html')

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
        self.assertFormError(response, 'login_form', None, 
            u'Wprowadź poprawną adres email oraz hasło. Uwaga: wielkość liter ma znaczenie.')

        response = self.client.post("/", {'login-password':'dump-password','login-username':'joe@doe.com'})
        self.assertFormError(response, 'login_form', None, 'To konto jest nieaktywne.')

        self.user.is_active = True
        self.user.is_superuser = True
        self.user.save()
        response = self.client.post("/", {'login-password':'dump-password','login-username':'joe@doe.com'})
        self.assertRedirects(response, '/admin/', status_code=302, target_status_code=200)

    def test_recover_password_step1(self):
        response = self.client.get("/reset_password/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password/reset.html')
        response = self.client.post("/reset_password/", {})
        self.assertFormError(response, 'form', 'email', 'To pole jest wymagane.')
        response = self.client.post("/reset_password/", {'email':'xxx'})
        self.assertFormError(response, 'form', 'email', u'Wprowadź poprawną nazwę użytkownika.')

        response = self.client.post("/reset_password/", {'email':'joe@doe.com'})
        self.assertRedirects(response, '/password_reset_done/', status_code=302, target_status_code=200)

    def test_recover_password_step2(self):
        response = self.client.get("/reset_password_confirm/MQ-3ng-31448e78548ea8785b65/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password/reset_confirm.html')

    def test_recover_password_step3(self):
        response = self.client.get("/password_reset_done/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password/reset_done.html')

    def test_recover_password_step4(self):
        response = self.client.get("/reset_password_complete/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password/reset_complete.html')

