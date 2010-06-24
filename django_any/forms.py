# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0103
"""
Django forms data generators

"""
import random
from django import forms
from django_any import xunit

class FormFieldDataFactory(object):
    """
    Registry storage for form field data functions

    Works like one parameter multimethod
    """
    def __init__(self):
        self.registry = {}

    def register(self, field_type, impl=None):
        """
        Register form field data function.
        
        Could be used as decorator
        """
        def _wrapper(func):
            self.registry[field_type] = func
            return func

        if impl:
            return _wrapper(impl)
        return _wrapper
    
    def decorator(self, impl):
        """
        Decorator for register decorators
        """
        self.__call__ = impl(self.__call__)
        return impl

    def __call__(self, *args, **kwargs):
        if not len(args):
            raise TypeError('Field instance are not provided')

        field_type = args[0].__class__

        function = self.registry.get(field_type)

        if function is None:
            raise TypeError("no match %s" % field_type)

        return function(*args, **kwargs)

any_form_field = FormFieldDataFactory()


def any_form(form_cls, **kwargs):
    """
    Returns tuple of form data and files
    """
    form_data = {}
    form_files = {}

    for name, field in form_cls.base_fields.iteritems():
        form_data[name] = any_form_field(field)

    return form_data, form_files


@any_form_field.decorator
def field_required_attribute(function):
    """
    Sometimes return None if field is not required

    >>> result = any_form_field(forms.BooleanField(required=False))
    >>> result in [None, True, False]
    True
    """
    def _wrapper(field, **kwargs):
        if not field.required and random.random < 0.1:
            return None
        return function(field, **kwargs)
    return _wrapper


@any_form_field.register(forms.BooleanField)
def boolean_field_data(field, **kwargs):
    """
    Return random value for BooleanField

    >>> result = any_form_field(forms.BooleanField())
    >>> type(result)
    <type 'bool'>
    """
    return xunit.any_boolean()


@any_form_field.register(forms.CharField)
def char_field_data(field, **kwargs):
    """
    Return random value for CharField
    >>> result = any_form_field(forms.CharField(min_length=3, max_length=10))
    >>> type(result)
    <type 'str'>
    """
    return xunit.any_string(min_length=field.min_length or 1, 
                            max_length=field.max_length or 255)

@any_form_field.register(forms.DecimalField)
def decimal_field_data(field, **kwargs):
    """
    Return random value for DecimalField

    >>> result = any_form_field(forms.DecimalField(max_value=100, min_value=11, max_digits=4, decimal_places = 2))
    >>> type(result)
    <class 'decimal.Decimal'>
    >>> from decimal import Decimal
    >>> result >= 11, result <= Decimal('99.99')
    (True, True)
    """
    min_value = 0
    max_value = 10
    from django.core.validators import MinValueValidator, MaxValueValidator 
    for elem in field.validators:
        if isinstance(elem, MinValueValidator):
            min_value = elem.limit_value
        if isinstance(elem, MaxValueValidator):
            max_value = elem.limit_value
    if (field.max_digits and field.decimal_places):
        from decimal import Decimal
        max_value = min(max_value,
                        Decimal('%s.%s' % ('9'*(field.max_digits-field.decimal_places),
                                           '9'*field.decimal_places)))
    return xunit.any_decimal(min_value=min_value,
                             max_value=max_value,
                             decimal_places = field.decimal_places or 2)

@any_form_field.register(forms.EmailField)
def email_field_data(field, **kwargs):
    """
    Return random value for EmailField

    >>> result = any_form_field(forms.EmailField(min_length=10, max_length=30))
    >>> type(result)
    <type 'str'>
    >>> len(result) <= 30, len(result) >= 10
    (True, True)
    """
    max_length = 10
    if field.max_length:
        max_length = (field.max_length -5) / 2 
    min_length = 10
    if field.min_length:
        min_length = (field.min_length-4) / 2
    return "%s@%s.%s" % (
        xunit.any_string(min_length=min_length, max_length=max_length),
        xunit.any_string(min_length=min_length, max_length=max_length),
        xunit.any_string(min_length=2, max_length=3))

"""@any_form_field.register(forms.DateField)
def date_field_data(field, **kwargs):
    """"""
    Return random value for DateField

    >>> result = any_form_field(forms.DateField(input_formats='%d %B %Y'))
    >>> type(result)
    <type 'datetime.date'>
    """"""
    date = xunit.any_date()
    if field.input_formats:
        date = date.strftime(field.input_formats)
    return date
"""

@any_form_field.register(forms.FloatField)
def float_field_data(field, **kwargs):
    """
    Return random value for FloatField

    >>> result = any_form_field(forms.FloatField(max_value=200, min_value=100))
    >>> type(result)
    <type 'float'>
    >>> result >=100, result <=200
    (True, True)
    """
    min_value = 0
    max_value = 100
    from django.core.validators import MinValueValidator, MaxValueValidator 
    for elem in field.validators:
        if isinstance(elem, MinValueValidator):
            min_value = elem.limit_value
        if isinstance(elem, MaxValueValidator):
            max_value = elem.limit_value
    return xunit.any_float(min_value=min_value, max_value=max_value, precision=3)

@any_form_field.register(forms.IntegerField)
def integer_field_data(field, **kwargs):
    """
    Return random value for IntegerField

    >>> result = any_form_field(forms.IntegerField(max_value=200, min_value=100))
    >>> type(result)
    <type 'int'>
    >>> result >=100, result <=200
    (True, True)
    """
    min_value = 0
    max_value = 100
    from django.core.validators import MinValueValidator, MaxValueValidator 
    for elem in field.validators:
        if isinstance(elem, MinValueValidator):
            min_value = elem.limit_value
        if isinstance(elem, MaxValueValidator):
            max_value = elem.limit_value
    return xunit.any_int(min_value=min_value, max_value=max_value)

@any_form_field.register(forms.IPAddressField)
def ipaddress_field_data(field, **kwargs):
    """
    Return random value for IPAddressField
    >>> result = any_form_field(forms.IPAddressField())
    >>> type(result)
    <type 'str'>
    >>> from django.core.validators import ipv4_re
    >>> import re
    >>> re.match(ipv4_re, result) is not None
    True
    """
    nums = [str(xunit.any_int(min_value=0, max_value=255)) for _ in xrange(0, 4)]
    return ".".join(nums)
