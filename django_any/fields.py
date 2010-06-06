#-*- coding: utf-8 -*-
"""
Values generators for common Django Fields
"""
import random
from decimal import Decimal
from django.db import models

import xunit
from multimethod import multimethod, multimethod_decorator

@multimethod_decorator
def any(function):
    """
    Sometimes return None if field could be blank
    """
    def wrapper(field, **kwargs):
        if field.blank and random.random < 0.1:
            return None
        return function(field, **kwargs)
    return wrapper


@multimethod_decorator
def any(function):
    """
    Selection from field.choices

    >>> CHOICES = [('YNG', 'Child'), ('OLD', 'Parent')]
    >>> result = any(models.CharField(max_length=3, choices=CHOICES))
    >>> result in ['YNG', 'OLD']
    True
    """
    def _valid_choices(choices):
        for key, value in choices:
            if isinstance(value, (list, tuple)):
                for key, item in value:
                    yield key
            else:
                yield key

    def wrapper(field, **kwargs):
        if field.choices:
            return random.choice(list(_valid_choices(field.choices)))
        return function(field, **kwargs)

    return wrapper


@multimethod(models.BooleanField)
def any(field, **kwargs):
    """
    Return random value for BooleanField

    >>> result = any(models.BooleanField())
    >>> type(result)
    <type 'bool'>
    """
    return xunit.any_boolean()


@multimethod(models.PositiveIntegerField)
def any(field, **kwargs):
    xunit.any_int(min_value=0, max_value=9999)


@multimethod(models.DecimalField)
def any(field, **kwargs):
    min_value = 0
    max_value = Decimal('%s.%s' % ('9'*(field.max_digits-field.decimal_places),
                                   '9'*field.decimal_places))
    return xunit.any_decimal(min_value=min_value, max_value=max_value,
                             decimal_places = field.decimal_places)


@multimethod(models.CharField)
def any(field, **kwargs):
    """
    Return random value for CharField

    >>> result = any(models.CharField(max_length=10))
    >>> type(result)
    <type 'str'>
    """
    return xunit.any_string(min_length=1, max_length=field.max_length)


@multimethod(models.DateField)
def any(field, **kwargs):
    return xunit.any_date()


@multimethod(models.DateTimeField)
def any(field, **kwargs):
    return xunit.any_datetime()


@multimethod(models.EmailField)
def any(field, **kwargs):
    return "%s@%s.%s" % (xunit.any_string(max_length=10),
                         xunit.any_string(max_length=10),
                         xunit.any_string(min_length=2, max_length=3))



