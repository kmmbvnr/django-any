# -*- coding: utf-8; mode: django -*-
"""
Test model creation with custom field validation
"""
from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase
from django_any import any_model


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(u'%s is not an even number' % value)


class ModelWithValidatedField(models.Model):
    even_field = models.PositiveIntegerField(validators=[validate_even])

    class Meta:
        app_label = 'django_any'    


class PassFieldValidation(TestCase):
    def test_created_value_pass_validation(self):
        result = any_model(ModelWithValidatedField)
        validate_even(result.even_field)

