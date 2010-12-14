# -*- coding: utf-8 -*-
from django import forms
from django.test import TestCase
from django_any import xunit
from django_any.forms import any_form

class TestForm(forms.Form):
    name = forms.CharField()


class TestFormDataCreation(TestCase):
    def test_simple_form_creation_succeed(self):
        data, _ = any_form(TestForm)
        self.assertTrue("name" in data)

    def test_set_field_value_secceed(self):
        some_value = xunit.any_string()
        data, _ = any_form(TestForm, name=some_value)
        self.assertTrue("name" in data)
        self.assertEqual(some_value, data["name"])

