# -*- coding: utf-8 -*-
from django import forms
from django.conf.urls.defaults import patterns
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, RequestContext
from django.test import TestCase
from django_any import xunit
from django_any.forms import any_form
from django_any.test import Client

class TestForm(forms.Form):
    name = forms.CharField()


def test_form_view(request):
    form = TestForm(request.POST or None)
    template = Template("{{ form }}")
    context = RequestContext(request, { 'form' : form })
    if form.is_valid():
        return HttpResponseRedirect('/')
    return HttpResponse(template.render(context))


urlpatterns = patterns('',
    (r'^test_form/', test_form_view))


class TestFormDataCreation(TestCase):
    urls = 'django_any.tests.any_forms_tests'

    def setUp(self):
        self.client = Client()

    def test_simple_form_creation_succeed(self):
        data, _ = any_form(TestForm)
        self.assertTrue("name" in data)

    def test_set_field_value_succeed(self):
        some_value = xunit.any_string()
        data, _ = any_form(TestForm, name=some_value)
        self.assertTrue("name" in data)
        self.assertEqual(some_value, data["name"])

    def test_post_any_data_with_implicit_forms_succeed(self):
        response = self.client.post_any_data('/test_form/')
        self.assertEquals(302, response.status_code)

    def test_post_any_data_with_explicit_forms_succeed(self):
        response = self.client.post_any_data('/test_form/', context_forms=['form'])
        self.assertEquals(302, response.status_code)

