#-*- coding: utf-8 -*-
# pylint: disable=E0102, W0613
"""
Values generators for common Django Fields
"""

import random
from decimal import Decimal
from django.db import models

from django_any import xunit
from django_any.multimethod import multimethod, multimethod_decorator

@multimethod_decorator('any_field')
def any_field_blank(function):
    """
    Sometimes return None if field could be blank
    """
    def wrapper(field, **kwargs):
        if field.blank and random.random < 0.1:
            return None
        return function(field, **kwargs)
    return wrapper


@multimethod_decorator('any_field')
def any_field_choices(function):
    """
    Selection from field.choices

    >>> CHOICES = [('YNG', 'Child'), ('OLD', 'Parent')]
    >>> result = any_field(models.CharField(max_length=3, choices=CHOICES))
    >>> result in ['YNG', 'OLD']
    True
    """
    def _valid_choices(choices):
        for key, value in choices:
            if isinstance(value, (list, tuple)):
                for key, _ in value:
                    yield key
            else:
                yield key

    def wrapper(field, **kwargs):
        if field.choices:
            return random.choice(list(_valid_choices(field.choices)))
        return function(field, **kwargs)

    return wrapper


@multimethod(models.BigIntegerField)
def any_field(field, **kwargs):
    """
    Return random value for BigIntegerField

    >>> result = any_field(models.BigIntegerField())
    >>> type(result)
    <type 'long'>
    """
    return long(xunit.any_int(min_value=1, max_value=10**20))


@multimethod(models.BooleanField)
def any_field(field, **kwargs):
    """
    Return random value for BooleanField

    >>> result = any_field(models.BooleanField())
    >>> type(result)
    <type 'bool'>
    """
    return xunit.any_boolean()


@multimethod(models.PositiveIntegerField)
def any_field(field, **kwargs):
    """
    An positive integer

    >>> result = any_field(models.PositiveIntegerField())
    >>> type(result)
    <type 'int'>
    >>> result > 0
    True
    """
    return xunit.any_int(min_value=1, max_value=9999)


@multimethod(models.CharField)
def any_field(field, **kwargs):
    """
    Return random value for CharField

    >>> result = any_field(models.CharField(max_length=10))
    >>> type(result)
    <type 'str'>
    """
    return xunit.any_string(min_length=1, max_length=field.max_length)


@multimethod(models.CommaSeparatedIntegerField)
def any_field(field, **kwargs):
    """
    Return random value for CharField

    >>> result = any_field(models.CommaSeparatedIntegerField(max_length=10))
    >>> type(result)
    <type 'str'>
    >>> [int(num) for num in result.split(',')] and 'OK'
    'OK'
    """
    nums_count = field.max_length/2
    nums = [str(xunit.any_int(min_value=0, max_value=9)) for _ in xrange(0, nums_count)]
    return ",".join(nums)


@multimethod(models.DecimalField)
def any_field(field, **kwargs):
    """
    Decimal value

    >>> result = any_field(models.DecimalField(max_digits=5, decimal_places=2))
    >>> type(result)
    <class 'decimal.Decimal'>
    """
    min_value = 0
    max_value = Decimal('%s.%s' % ('9'*(field.max_digits-field.decimal_places),
                                   '9'*field.decimal_places))
    return xunit.any_decimal(min_value=min_value, max_value=max_value,
                             decimal_places = field.decimal_places)


@multimethod(models.DateField)
def any_field(field, **kwargs):
    return xunit.any_date()


@multimethod(models.DateTimeField)
def any_field(field, **kwargs):
    return xunit.any_datetime()


@multimethod(models.EmailField)
def any_field(field, **kwargs):
    return "%s@%s.%s" % (xunit.any_string(max_length=10),
                         xunit.any_string(max_length=10),
                         xunit.any_string(min_length=2, max_length=3))

