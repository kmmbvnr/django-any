# -*- coding: utf-8 -*-
from django.test import TestCase
from django.db import models
from django_any import fields

class TestChoiceSelection(TestCase):
    def test_one_case_selection(self):
        field = models.BooleanField(choices=[(False, 'This sentence is wrong')])
        result = fields.any(field)
        assert type(result) == bool
        assert result is False     

    def test_two_case_selection(self):
        field = models.CharField(max_length=3, choices=[('YNG', 'Child'),
                                                        ('OLD', 'Parent')])
        result = fields.any(field)
        assert type(result) == str
        assert result in ['YNG', 'OLD']
