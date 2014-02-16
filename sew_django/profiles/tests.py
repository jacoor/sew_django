# -*- coding: utf-8 -*-
from django.test import TestCase
#from django.core.urlresolvers import reverse
from django.test.client import Client

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.forms.models import model_to_dict

from sew_django.profiles.models import Profile
from sew_django.profiles.forms import RegisterUserFullForm, AdminRegisterUserFullForm
#from sew_django.profiles.views import Index


class ProfileTests(TestCase):
    CORRECT_PESEL = 84111508709
    CORRECT_PESEL_1 = 81101507348
    CORRECT_PESEL_2 = '02280710383'
    INVALID_PESEL = 1111111
    INVALID_PESEL_2 = '02280710382'

    REGISTER_FULL_EXPECTED_FORM_FIELDS = [
        'pesel',
        'email',
        'photo',
        'first_name',
        'last_name',
        'street',
        'house',
        'flat',
        'zip',
        'city',
        'phone',
        'workplace_name',
        'workplace_address',
        'workplace_zip',
        'workplace_city',
        'password',
        'password_confirm',
        'consent_processing_of_personal_data',
        'accept_of_sending_data_to_WOSP']

    REGISTER_FULL_ADMIN_EXPECTED_REQUIRED_FORM_FIELDS = [
        'pesel',
        'email',
        'first_name',
        'last_name',
        'street',
        'house',
        'zip',
        'city',
        'phone',
        'password',
        'password_confirm']

    REGISTER_FULL_PUBLIC_EXPECTED_REQUIRED_FORM_FIELDS = REGISTER_FULL_ADMIN_EXPECTED_REQUIRED_FORM_FIELDS + [
        'consent_processing_of_personal_data',
        'accept_of_sending_data_to_WOSP']

    VALID_USER = {
        'pesel': '80010363616',
        'email': 'test@example.com',
        'first_name': 'Jan',
        'last_name': 'Kowalski',
        'street': u'przykładowa ulica o długiej nazwie',
        'house': u'przykładowy numer domu',
        'flat': u'nr lok.',
        'zip': '51-111',
        'city': u'Wrocław',
        'phone': u'przykładowy telefon',
        'workplace_name': u'nazwa zakład pracy',
        'workplace_address': u'adres zakładu pracy',
        'workplace_city': u'miejscowość zakładu pracy',
        'workplace_zip': '51-111',
        'password': '123456Aa',
        'password_confirm': '123456Aa',
        'consent_processing_of_personal_data': 'on',
        'accept_of_sending_data_to_WOSP': 'on',
    }

    def setUp(self):
        self.user = Profile.objects.create(
            first_name='Joe',
            username='joe',
            email='joe@doe.com',
            pesel=self.CORRECT_PESEL,
            is_active=False,)
        self.user.set_password('dump-password')
        self.user.save()

    def activate_user(self):
        self.user.is_active = True
        self.user.save()

    def test_create_user(self):
        user = Profile.objects.create_user(
            first_name='Joe',
            username='joe1',
            email='joe1@doe.com',
            pesel=self.CORRECT_PESEL_1,
            is_active=False,)
        user.set_password('dump-password')
        verify_user = Profile.objects.get_by_email('joe1@doe.com')
        self.assertEqual(verify_user.username, user.username)

    def test_create_super_user(self):
        user = Profile.objects.create_superuser(
            email='joe2@doe.com',
            password='dump-password',)

        verify_user = Profile.objects.get_by_email('joe2@doe.com')
        self.assertEqual(verify_user.username, user.username)

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

        response = self.client.post("/login/", {'login-username': 'xxx'})
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

    def test_admin_login_redirect(self):
        user = Profile.objects.create_superuser(
                                            email='joe2@doe.com',
                                            password='dump-password',
                                            )
        
        user.is_active = True
        user.save()
        response = self.client.post("/login/", {'login-password':'dump-password','login-username':'joe2@doe.com',})
        self.assertRedirects(response, settings.ADMIN_LOGIN_REDIRECT_URL, status_code=302, target_status_code=200)

    def test_different_domain_redirect(self):
        user = Profile.objects.create_superuser(
                                            email='joe2@doe.com',
                                            password='dump-password',
                                            )
        
        user.is_active = True
        user.save()
        response = self.client.post("/login/", {'login-password':'dump-password','login-username':'joe2@doe.com', 
            'next' : 'http://onet.pl/'})
        print response
        self.assertRedirects(response, settings.ADMIN_LOGIN_REDIRECT_URL, status_code=302, target_status_code=200)

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
        self.assertTemplateUsed(response, 'register/form.html')

    def test_register_step_1_empty(self):
        response = self.client.post("/rejestracja-wolontariusza/", {})
        self.assertFormError(response, 'pesel_form', 'pesel', 'To pole jest wymagane.')

    def test_register_step_1_invalid(self):
        response = self.client.post("/rejestracja-wolontariusza/", {'pesel-pesel': 'xxx'})
        self.assertFormError(response, 'pesel_form', 'pesel', u'Numer PESEL składa się z 11 cyfr.')

    def test_register_step_1_existing_pesel(self):
        response = self.client.post("/rejestracja-wolontariusza/", {'pesel-pesel': self.CORRECT_PESEL})
        self.assertFormError(response, 'pesel_form', 'pesel',
                             u'Numer PESEL już istnieje w naszej bazie. <a href="/login/">Zaloguj się</a>.')

    def test_register_step_1_proper_pesel(self):
        response = self.client.post("/rejestracja-wolontariusza/", {'pesel-pesel': self.CORRECT_PESEL_2})
        self.assertRedirects(response, '/rejestracja-wolontariusza/1/?pesel=%s' % self.CORRECT_PESEL_2,
                             status_code=302, target_status_code=200)

    def test_register_step_2_wo_pesel(self):
        response = self.client.get("/rejestracja-wolontariusza/1/",)
        self.assertRedirects(response, '/rejestracja-wolontariusza/', status_code=302, target_status_code=200)

    def test_register_step_2(self):
        response = self.client.get("/rejestracja-wolontariusza/1/", {'pesel': 'jakikolwiek'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/full.html')
        self.assertEqual(response.context['form'].initial.get('pesel'), 'jakikolwiek')

    def test_register_forms_confirm_password_fail(self):
        form = AdminRegisterUserFullForm(data={'password': 'passwordA2', 'password_confirm': "PasswordA3"})
        self.failIf(form.is_valid())
        self.assertIn(_("Passwords doesn't match."), form.errors['password_confirm'])

    def test_register_user_in_admin_form_fields(self):
        form = AdminRegisterUserFullForm()
        self.assertEqual(form.fields.keys(), self.REGISTER_FULL_EXPECTED_FORM_FIELDS)

    def test_register_user_in_admin_confirm_password_success(self):
        form = AdminRegisterUserFullForm(data={'password': 'passwordA2', 'password_confirm': "passwordA2"})
        self.failIf(form.is_valid())
        self.assertFalse(form.errors.get('password_confirm'))

    def test_empty_public_registration_form(self):
        #should throw all errors!
        form = RegisterUserFullForm(data={})
        self.failIf(form.is_valid())
        self.assertEqual(set(form.errors.keys()), set(self.REGISTER_FULL_PUBLIC_EXPECTED_REQUIRED_FORM_FIELDS))

    def test_empty_admin_registration_form(self):
        #should throw all errors!
        form = AdminRegisterUserFullForm(data={})
        self.failIf(form.is_valid())
        self.assertEqual(set(form.errors.keys()), set(self.REGISTER_FULL_ADMIN_EXPECTED_REQUIRED_FORM_FIELDS))

    def help_test_register_forms(self):
        #activate & login user
        user = Profile.objects.get_by_email(self.VALID_USER.get("email"))
        response = self.client.login(username=self.VALID_USER.get("email"), password=self.VALID_USER.get("password"))
        self.assertEqual(response, False)
        user.is_active = True
        user.save()
        response = self.client.login(username=self.VALID_USER.get("email"), password=self.VALID_USER.get("password"))
        self.assertEqual(response, True)
        user_for_compare = self.VALID_USER.copy()
        del user_for_compare['password']
        del user_for_compare['password_confirm']
        user_for_compare['accept_of_sending_data_to_WOSP'] = True
        user_for_compare['consent_processing_of_personal_data'] = True
        user_for_compare['username'] = user_for_compare['email']
        user_for_compare['read_only'] = False
        user_for_compare['is_active'] = True
        user_for_compare['is_superuser'] = False
        user_for_compare['is_staff'] = False
        user_for_compare['last_login'] = None
        user_for_compare['token'] = ''
        user_for_compare['photo'] = ''
        user_for_compare['is_active'] = True
        user_for_compare['rank'] = ''

        user_from_db = model_to_dict(user)
        del user_from_db['password']
        del user_from_db['id']
        del user_from_db['groups']
        del user_from_db['user_permissions']

        self.assertEqual(set(user_from_db), set(user_for_compare))

    def test_valid_public_user_reqistration(self):
        form = RegisterUserFullForm(data=self.VALID_USER)
        self.assertTrue(form.is_valid())
        form.save()
        self.help_test_register_forms()

    def test_valid_admin_user_reqistration(self):
        form = AdminRegisterUserFullForm(data=self.VALID_USER)
        self.assertTrue(form.is_valid())
        form.save()
        self.help_test_register_forms()
