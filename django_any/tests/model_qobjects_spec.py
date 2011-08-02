# -*- coding: utf-8; mode: django -*-
"""
Allow partial specifications with q objects
"""
from django.db import models
from django.db.models import Q
from django.test import TestCase
from django_any import any_model


class QObjectRelated(models.Model):
    class Meta:
        app_label = 'django_any'


class RelatedToQObject(models.Model):
    related = models.ForeignKey(QObjectRelated)

    class Meta:
        app_label = 'django_any'
    

class QObjectsSupport(TestCase):
    def setUp(self):
        self.related = any_model(QObjectRelated)
        
    def test_qobject_specification(self):
        result = any_model(RelatedToQObject, related=Q(pk=self.related.pk))
        self.assertEqual(self.related, result.related)

