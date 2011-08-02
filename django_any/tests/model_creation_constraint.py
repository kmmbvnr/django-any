# -*- coding: utf-8; mode: django -*-
"""
Models that have custom validation checks
"""
from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase
from django_any import any_model


class ModelWithConstraint(models.Model):
    """
    Validates that start_time is always before end_time
    """
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError('start_time could not be after end_time')

    class Meta:
        app_label = 'django_any'


class ModelWithConstraintOnForeignKey(models.Model):
    timestamp = models.ForeignKey(ModelWithConstraint)

    class Meta:
        app_label = 'django_any'


class PassModelValidation(TestCase):
    def test_model_creation_succeed(self):
        result = any_model(ModelWithConstraint)
        self.assertTrue(result.start_time <= result.end_time)

    def test_foreignkey_constraint_succeed(self):
        result = any_model(ModelWithConstraintOnForeignKey)
        self.assertTrue(result.timestamp.start_time <= result.timestamp.end_time)

