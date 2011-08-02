# -*- coding: utf-8; mode: django -*-
"""
Auto-create foreingkey referencies
"""
from django.db import models
from django.test import TestCase
from django_any import any_model


class RelatedModel(models.Model):
    name = models.CharField(max_length=5)

    class Meta:
        app_label = 'django_any'


class BaseModel(models.Model):
    related = models.ForeignKey(RelatedModel)

    class Meta:
        app_label = 'django_any'


class ForeignKeyCreation(TestCase):
    def test_fk_relation_autocreate(self):
        result = any_model(BaseModel)

        self.assertEqual(type(result), BaseModel)

        self.assertEqual(type(result.related), RelatedModel)
        self.assertTrue(result.related.name is not None)

    def test_nested_models_specification(self):
        result = any_model(BaseModel, related__name='test')
        self.assertEqual(result.related.name, 'test')

