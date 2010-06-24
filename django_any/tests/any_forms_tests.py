# -*- coding: utf-8 -*-
from django import forms
from django.test import TestCase
from django_any.forms import any_form

class TestForm(forms.Form):
    name = forms.CharField()


class TestFormDataCreation(TestCase):
    def test_simple_form_creation(self):
        data, files = any_form(TestForm)

        self.assertTrue("name" in data)

