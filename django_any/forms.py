# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0103
"""
Django forms data generators

"""
import random
from django import forms
from django_any import xunit
from django_any.functions import valid_choices, split_model_kwargs, \
    ExtensionMethod

any_form_field = ExtensionMethod()


def any_form(form_cls, **kwargs):
    """
    Returns tuple of form data and files
    """
    form_data = {}
    form_files = {}

    form_fields, fields_args = split_model_kwargs(kwargs)

    for name, field in form_cls.base_fields.iteritems():
        if name in form_fields:
            form_data[name] = kwargs[name]
        else:
            form_data[name] = any_form_field(field)

    return form_data, form_files


@any_form_field.decorator
def field_required_attribute(function):
    """
    Sometimes return None if field is not required

    >>> result = any_form_field(forms.BooleanField(required=False))
    >>> result in ['', 'True', 'False']
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
    <type 'str'>
    """
    return str(xunit.any_boolean())


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
    <type 'str'>
    >>> from decimal import Decimal
    >>> Decimal(result) >= 11, Decimal(result) <= Decimal('99.99')
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
    return str(xunit.any_decimal(min_value=min_value,
                             max_value=max_value,
                             decimal_places = field.decimal_places or 2))


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


@any_form_field.register(forms.DateField)
def date_field_data(field, **kwargs):
    """
    Return random value for DateField

    >>> result = any_form_field(forms.DateField())
    >>> type(result)
    <type 'str'>
    """
    date = xunit.any_date()
    if field.input_formats:
        date = date.strftime(field.input_formats)
    else:
        date = date.strftime('%Y-%m-%d')
    return date


@any_form_field.register(forms.DateTimeField)
def datetime_field_data(field, **kwargs):
    """
    Return random value for DateTimeField

    >>> result = any_form_field(forms.DateTimeField())
    >>> type(result)
    <type 'str'>
    """
    datetime = xunit.any_datetime()
    if field.input_formats:
        datetime = datetime.strftime(field.input_formats)
    else:
        datetime = datetime.strftime('%Y-%m-%d %H:%M:%S')
    return datetime


@any_form_field.register(forms.FloatField)
def float_field_data(field, **kwargs):
    """
    Return random value for FloatField

    >>> result = any_form_field(forms.FloatField(max_value=200, min_value=100))
    >>> type(result)
    <type 'str'>
    >>> float(result) >=100, float(result) <=200
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
    return str(xunit.any_float(min_value=min_value, max_value=max_value, precision=3))


@any_form_field.register(forms.IntegerField)
def integer_field_data(field, **kwargs):
    """
    Return random value for IntegerField

    >>> result = any_form_field(forms.IntegerField(max_value=200, min_value=100))
    >>> type(result)
    <type 'str'>
    >>> int(result) >=100, int(result) <=200
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
    return str(xunit.any_int(min_value=min_value, max_value=max_value))


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


@any_form_field.register(forms.NullBooleanField)
def null_boolean_field_data(field, **kwargs):
    """
    Return random value for NullBooleanField
    
    >>> result = any_form_field(forms.NullBooleanField())
    >>> type(result)
    <type 'str'>
    >>> result in ['None', 'True', 'False']
    True
    """
    return random.choice(['None', 'True', 'False'])


@any_form_field.register(forms.SlugField)
def slug_field_data(field, **kwargs):
    """
    Return random value for SlugField
    
    >>> result = any_form_field(forms.SlugField())
    >>> type(result)
    <type 'str'>
    >>> from django.core.validators import slug_re
    >>> import re
    >>> re.match(slug_re, result) is not None
    True
    """
    from string import ascii_letters, digits
    letters = ascii_letters + digits + '_-' 
    return xunit.any_string(letters = letters, max_length = 20)


@any_form_field.register(forms.URLField)
def url_field_data(field, **kwargs):
    """
    Return random value for URLField
    
    >>> result = any_form_field(forms.URLField())
    >>> from django.core.validators import URLValidator
    >>> import re
    >>> re.match(URLValidator.regex, result) is not None
    True
    """
    url = ['http://news.yandex.ru/society.html',
           'http://video.google.com/?hl=en&tab=wv',
           'http://www.microsoft.com/en/us/default.aspx',
           'http://habrahabr.ru/company/opera/',
           'http://www.apple.com/support/hardware/',
           'http://localhost/',
           'http://72.14.221.99',
           'http://fr.wikipedia.org/wiki/France']
    from random import choice
    return choice(url)


@any_form_field.register(forms.TimeField)
def time_field_data(field, **kwargs):
    """
    Return random value for TimeField

    >>> result = any_form_field(forms.TimeField())
    >>> type(result)
    <type 'str'>
    """
    import datetime
    time = datetime.time(xunit.any_int(min_value=0, max_value=23),
                         xunit.any_int(min_value=0, max_value=59),
                         xunit.any_int(min_value=0, max_value=59))
    if field.input_formats:
        time = time.strftime(field.input_formats)
    else:
        time = time.strftime('%H:%M:%S')
    return time


@any_form_field.register(forms.TypedChoiceField)
@any_form_field.register(forms.ChoiceField)
def choice_field_data(field, **kwargs):
    """
    Return random value for ChoiceField

    >>> CHOICES = [('YNG', 'Child'), ('OLD', 'Parent')]
    >>> result = any_form_field(forms.ChoiceField(choices=CHOICES))
    >>> type(result)
    <type 'str'>
    >>> result in ['YNG', 'OLD']
    True
    >>> typed_result = any_form_field(forms.TypedChoiceField(choices=CHOICES))
    >>> typed_result in ['YNG', 'OLD']
    True
    """
    if field.choices:
        return str(random.choice(list(valid_choices(field.choices))))
    return 'None'


@any_form_field.register(forms.MultipleChoiceField)
def multiple_choice_field_data(field, **kwargs):
    """
    Return random value for MultipleChoiceField

    >>> CHOICES = [('YNG', 'Child'), ('MIDDLE', 'Parent') ,('OLD', 'GrandParent')]
    >>> result = any_form_field(forms.MultipleChoiceField(choices=CHOICES))
    >>> type(result)
    <type 'str'>
    """
    if field.choices:
        from django_any.functions import valid_choices 
        l = list(valid_choices(field.choices))
        random.shuffle(l)
        choices = []
        count = xunit.any_int(min_value=1, max_value=len(field.choices))
        for i in xrange(0, count):
            choices.append(l[i])
        return ' '.join(choices)
    return 'None'

