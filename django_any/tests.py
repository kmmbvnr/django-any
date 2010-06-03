#-*- coding: utf-8 -*-
import doctest
from unittest import TestSuite, defaultTestLoader
from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User

from django_any import fields
from django_any.models import any_model

class SimpleModel(models.Model):
    name = models.CharField(max_length=5)
    

class ModelWithForeignKey(models.Model):
    name = models.CharField(max_length=5)
    simple = models.ForeignKey(SimpleModel)


class TestAnyModel(TestCase):
    def test_simple_model_creation(self):
        result = any_model(SimpleModel)
        assert type(result) == SimpleModel
        assert result.name is not None

    def test_foreign_key_creation(self):
        result = any_model(ModelWithForeignKey)
        assert type(result) == ModelWithForeignKey
        assert type(result.simple) == SimpleModel
        assert result.name is not None
        assert result.simple.name is not None

    def test_user_creation(self):
        result = any_model(User)

    def test_set_nested_fields(self):
        result = any_model(ModelWithForeignKey, simple__name='SimpleName')
        self.assertEqual('SimpleName', result.simple.name)


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


def suite():
    suite = TestSuite()
    suite.addTest(defaultTestLoader.loadTestsFromTestCase(TestAnyModel))
    suite.addTest(doctest.DocTestSuite('django_any.xunit'))
    suite.addTest(doctest.DocTestSuite('django_any.fields'))
    suite.addTest(doctest.DocTestSuite('django_any.multimethod'))
    
    return suite
