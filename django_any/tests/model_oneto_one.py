# -*- coding: utf-8; mode: django -*-
"""
Shortcuts for onetoone model fields
"""
from django.db import models
from django.test import TestCase
from django_any import any_model


class OneToOneRelated(models.Model):
    name = models.CharField(max_length=5)

    class Meta:
        app_label = 'django_any'


class ModelWithOneToOneField(models.Model):
    name = models.CharField(max_length=5)
    related = models.OneToOneField(OneToOneRelated)

    class Meta:
        app_label = 'django_any'


class OneToOneCreation(TestCase):
    def test_oneto_one_autocreate(self):
        result = any_model(ModelWithOneToOneField)
        self.assertEqual(type(result), ModelWithOneToOneField)
        self.assertTrue(result.name is not None)

        self.assertEqual(type(result.related), OneToOneRelated)
        self.assertTrue(result.related.name is not None)

    def test_related_onetoone_not_created_by_default(self):
        simple_model = any_model(OneToOneRelated)
        self.assertRaises(ModelWithOneToOneField.DoesNotExist,
                          lambda : simple_model.modelwithonetoonefield)

    def test_related_specification_succeed(self):
        related = any_model(OneToOneRelated)
        result = any_model(ModelWithOneToOneField, related=related)
        self.assertEqual(related, result.related)

    def test_partial_specification_succeed(self):
        result = any_model(ModelWithOneToOneField, related__name='test')
        self.assertEqual(result.related.name, 'test')

    # TODO Create model for reverse relation
    def _test_reverse_relation_spec_succeed(self):
        related = any_model(OneToOneRelated, modelwithonetoonefield__name='test')
        self.assertEqual(related.modelwithonetoonefield.name, 'test')

