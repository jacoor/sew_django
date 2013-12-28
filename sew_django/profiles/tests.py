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
    CORRECT_PESEL=84111508709
    CORRECT_PESEL_1=81101507348
    CORRECT_PESEL_2='02280710383'
    INVALID_PESEL=1111111
    INVALID_PESEL_2='02280710382'

    def setUp(self):
        self.user = Profile.objects.create(first_name='Joe',
                                            username ='joe',
                                            email='joe@doe.com',
                                            pesel=self.CORRECT_PESEL,
                                            is_active=False,
                                            )
        self.user.set_password('dump-password')
        self.user.save()
    
    def activate_user(self):
        self.user.is_active = True
        self.user.is_superuser = True
        self.user.save()

    def test_create_user(self):
        user = Profile.objects.create_user(first_name='Joe',
                                            username ='joe1',
                                            email='joe1@doe.com',
                                            pesel=self.CORRECT_PESEL_1,
                                            is_active=False,
                                            )
        user.set_password('dump-password')

        verify_user = Profile.objects.get_by_email('joe1@doe.com')
        self.assertEqual(verify_user.username, user.username)

    def test_create_super_user(self):
        user = Profile.objects.create_superuser(
                                            email='joe2@doe.com',
                                            password='dump-password',
                                            )

        verify_user = Profile.objects.get_by_email('joe2@doe.com')
        self.assertEqual(verify_user.username, user.username)

    def test_create_user_wo_email(self):

        with self.assertRaises(ValueError) as cm:
            user = Profile.objects.create_user(first_name='Joe',
                                                username ='joe2',
                                                pesel=self.CORRECT_PESEL_1,
                                                is_active=False,
                                                )
            user.set_password('dump-password')
            
            user.save()

    def test_index(self):
        #request = RequestFactory().get(reverse('index'))
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_login_view(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logout(self):
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/', status_code=301, target_status_code=200)

    def test_login(self):
        #request = RequestFactory().get(reverse('index'))
        response = self.client.login(username='joe', password='dump-password')
        self.assertEqual(response, False) 
        self.user.is_active = True
        self.user.save()
        response = self.client.login(username='joe', password='dump-password')
        self.assertEqual(response, True)

    def test_login_form_view(self):
        response = self.client.post("/login/", {})
        self.assertFormError(response, 'login_form', 'password', 'To pole jest wymagane.')
        self.assertFormError(response, 'login_form', 'username', 'To pole jest wymagane.')

        response = self.client.post("/login/", {'login-username':'xxx'})
        self.assertFormError(response, 'login_form', 'password', 'To pole jest wymagane.')
        
        response = self.client.post("/login/", {'login-password':'xxx'})
        self.assertFormError(response, 'login_form', 'username', 'To pole jest wymagane.')

        response = self.client.post("/login/", {'login-password':'xxx','login-username':'xxx'})
        self.assertFormError(response, 'login_form', None, 
            u"Wprowadź poprawny numer PESEL lub adres email.")

    def test_invalid_login(self):
        response = self.client.post("/login/", {'login-password':'dump-password','login-username':'joe'})
        self.assertFormError(response, 'login_form', None, 'To konto jest nieaktywne.')

    def test_login_and_redirect(self):
        self.activate_user()
        response = self.client.post("/login/", {'login-password':'dump-password','login-username':'joe', \
            'next' :'/none/'})
        self.assertRedirects(response, '/none/', status_code=302, target_status_code=404)

    def test_login_by_username(self):
        self.activate_user()
        response = self.client.post("/login/", {'login-password':'dump-password','login-username':'joe'})
        self.assertRedirects(response, '/profil/', status_code=302, target_status_code=200)

    def test_login_by_email(self):
        self.activate_user()
        response = self.client.post("/login/", {'login-password':'dump-password','login-username':'joe@doe.com'})
        self.assertRedirects(response, '/profil/', status_code=302, target_status_code=200)

    def test_login_by_pesel(self):
        self.activate_user()
        response = self.client.post("/login/", {'login-password':'dump-password','login-username':self.CORRECT_PESEL})
        self.assertRedirects(response, '/profil/', status_code=302, target_status_code=200)
        
    def test_recover_password_step1(self):
        response = self.client.get("/reset_password/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password/reset.html')

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

    def test_pesel_form_view(self):
        c = Client()
        response = c.get('/rejestracja-wolontariusza/')
        #w/o pesel should show pesel form
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/step_1_pesel.html')

    def test_register_step_1_empty(self):
        response = self.client.post("/rejestracja-wolontariusza/", {})
        self.assertFormError(response, 'pesel_form', 'pesel', 'To pole jest wymagane.')

    def test_register_step_1_invalid(self):
        response = self.client.post("/rejestracja-wolontariusza/", {'pesel-pesel':'xxx'})
        self.assertFormError(response, 'pesel_form', 'pesel', u'Numer PESEL składa się z 11 cyfr.')
       
    def test_register_step_1_invalid(self):
        response = self.client.post("/rejestracja-wolontariusza/", {'pesel-pesel':self.INVALID_PESEL_2})
        self.assertFormError(response, 'pesel_form', 'pesel', u'Błędna suma kontrolna numeru PESEL.')
