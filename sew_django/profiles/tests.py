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
                                            is_active=True)
        self.user.set_password('dump-password')
        self.user.save()

    def test_index(self):
        #request = RequestFactory().get(reverse('index'))
        c = Client()
        response = c.get('/')
        #response.status_code
        self.assertEqual(response.status_code, 200)

