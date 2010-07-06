# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from django.test import TestCase
from django_any.test import Client


urlpatterns = patterns('',
     (r'^admin/', include(admin.site.urls)),
)

class TestDjangoAnyClient(TestCase):
    urls = 'django_any.tests.test_client_tests'

    def setUp(self):
        self.client = Client()

    def test_login_as_super_user(self):        
        self.assertTrue(self.client.login_as(is_superuser=True))

        response = self.client.get('/admin/')
        self.assertEquals(200, response.status_code)

