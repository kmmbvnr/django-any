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


@multimethod(models.DateField)
def any_field(field, **kwargs):
    """
    Return random value for DateField, 
    skips auto_now and auto_now_add fields

    >>> result = any_field(models.DateField())
    >>> type(result)
    <type 'datetime.date'>
    """
    if field.auto_now or field.auto_now_add:
        return None
    return xunit.any_date()


@multimethod(models.DateTimeField)
def any_field(field, **kwargs):
    """
    Return random value for DateTimeField, 
    skips auto_now and auto_now_add fields

    >>> result = any_field(models.DateTimeField())
    >>> type(result)
    <type 'datetime.datetime'>
    """
    return xunit.any_datetime()


@multimethod(models.DecimalField)
def any_field(field, **kwargs):
    """
    Return random value for DecimalField

    >>> result = any_field(models.DecimalField(max_digits=5, decimal_places=2))
    >>> type(result)
    <class 'decimal.Decimal'>
    """
    min_value = 0
    max_value = Decimal('%s.%s' % ('9'*(field.max_digits-field.decimal_places),
                                   '9'*field.decimal_places))
    return xunit.any_decimal(min_value=min_value, max_value=max_value,
                             decimal_places = field.decimal_places)


@multimethod(models.EmailField)
def any_field(field, **kwargs):
    """
    Return random value for EmailField

    >>> result = any_field(models.EmailField())
    >>> type(result)
    <type 'str'>
    >>> import re
    >>> re.match(r"(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)", result, re.IGNORECASE) is not None
    True
    """
    return "%s@%s.%s" % (xunit.any_string(max_length=10),
                         xunit.any_string(max_length=10),
                         xunit.any_string(min_length=2, max_length=3))

@multimethod(models.FloatField)
def any_field(field, **kwargs):
    """
    Return random value for FloatField

    >>> result = any_field(models.FloatField())
    >>> type(result)
    <type 'float'>
    """
    return xunit.any_float(min_value=1, max_value=100, precision=3)

@multimethod(models.IPAddressField)
def any_field(field, **kwargs):
    """
    Return random value for IPAddressField
    >>> result = any_field(models.IPAddressField())
    >>> type(result)
    <type 'str'>
    >>> from django.core.validators import ipv4_re
    >>> import re
    >>> re.match(ipv4_re, result) is not None
    True
    """
    nums = [str(xunit.any_int(min_value=0, max_value=255)) for _ in xrange(0, 4)]
    return ".".join(nums)

@multimethod(models.NullBooleanField)
def any_field(field, **kwargs):
    """
    Return random value for IPAddressField
    >>> result = any_field(models.NullBooleanField())
    >>> result in [None, True, False]
    True
    """
    return random.choice([None, True, False])


    
