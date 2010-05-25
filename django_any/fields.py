#-*- coding: utf-8 -*-
"""
Values generators for common Django Fields
"""
from django.db import models
from multimethod import multimethod
from decimal import Decimal
import xunit


@multimethod(models.BooleanField)
def any(field, **kwargs):
    """
    Return random value for BooleanField
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


__test__ = {"common":
"""
>>> result = any(models.BooleanField())
>>> type(result)
<type 'bool'>
>>> result = any(models.CharField(max_length=10))
>>> type(result)
<type 'str'>
"""}
