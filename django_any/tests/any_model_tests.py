# -*- coding: utf-8 -*-
from django.db import models, IntegrityError
from django.test import TestCase
from django_any.models import any_model

class SimpleModel(models.Model):
    name = models.CharField(max_length=5)

    class Meta:
        app_label='django_any'


class ModelWithForeignKey(models.Model):
    name = models.CharField(max_length=5)
    simple = models.ForeignKey(SimpleModel)

    class Meta:
        app_label='django_any'


class ModelWithOneChoice(models.Model):
    CHOICES = [('N', 'No')]
    choice = models.CharField(max_length=1, choices=CHOICES, unique=True)

    class Meta:
        app_label='django_any'


class ModelWithTwoChoices(models.Model):
    CHOICES = [('Y', 'Yes'),
               ('N', 'No')]
    choice = models.CharField(max_length=1, choices=CHOICES, unique=True)

    class Meta:
        app_label='django_any'


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
        #TODO move to integration tests
        from django.contrib.auth.models import User
        result = any_model(User)

    def test_set_nested_fields(self):
        result = any_model(ModelWithForeignKey, simple__name='SimpleName')
        self.assertEqual('SimpleName', result.simple.name)


class TestUniqueConstrainViolations(TestCase):
    def test_fail_if_no_choices(self):
        ModelWithOneChoice.objects.create(choice='N')
        self.assertRaises(IntegrityError, any_model, ModelWithOneChoice)

    def test_unique_generation_succedd(self):
        ModelWithTwoChoices.objects.create(choice='N')
        
        result = any_model(ModelWithTwoChoices)
        self.assertEqual('Y', result.choice)

