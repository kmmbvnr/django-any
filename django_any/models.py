#-*- coding: utf-8 -*-
# pylint: disable=E0102, W0613
"""
Values generators for common Django Fields
"""
import re, os, random
from decimal import Decimal
from datetime import date, datetime, time
from string import ascii_letters, digits
from random import choice

from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.db.models import Q
from django.db.models.fields.files import FieldFile
from django.contrib.webdesign.lorem_ipsum import paragraphs

from django_any import xunit
from django_any.functions import valid_choices, split_model_kwargs, \
    ExtensionMethod

any_field = ExtensionMethod()
any_model = ExtensionMethod()

@any_field.decorator
def any_field_blank(function):
    """
    Sometimes return None if field could be blank
    """
    def wrapper(field, **kwargs):
        if kwargs.get('isnull', False):
            return None
    
        if field.blank and random.random < 0.1:
            return None
        return function(field, **kwargs)
    return wrapper


@any_field.decorator
def any_field_choices(function):
    """
    Selection from field.choices

    >>> CHOICES = [('YNG', 'Child'), ('OLD', 'Parent')]
    >>> result = any_field(models.CharField(max_length=3, choices=CHOICES))
    >>> result in ['YNG', 'OLD']
    True
    """
    def wrapper(field, **kwargs):
        if field.choices:
            return random.choice(list(valid_choices(field.choices)))
        return function(field, **kwargs)

    return wrapper


@any_field.register(models.BigIntegerField)
def any_biginteger_field(field, **kwargs):
    """
    Return random value for BigIntegerField

    >>> result = any_field(models.BigIntegerField())
    >>> type(result)
    <type 'long'>
    """
    min_value = kwargs.get('min_value', 1)
    max_value = kwargs.get('max_value', 10**20)
    return long(xunit.any_int(min_value=min_value, max_value=max_value))


@any_field.register(models.BooleanField)
def any_boolean_field(field, **kwargs):
    """
    Return random value for BooleanField

    >>> result = any_field(models.BooleanField())
    >>> type(result)
    <type 'bool'>
    """
    return xunit.any_boolean()


@any_field.register(models.PositiveIntegerField)
def any_positiveinteger_field(field, **kwargs):
    """
    An positive integer

    >>> result = any_field(models.PositiveIntegerField())
    >>> type(result)
    <type 'int'>
    >>> result > 0
    True
    """
    min_value = kwargs.get('min_value', 1)
    max_value = kwargs.get('max_value', 9999)
    return xunit.any_int(min_value=min_value, max_value=max_value)


@any_field.register(models.CharField)
def any_char_field(field, **kwargs):
    """
    Return random value for CharField

    >>> result = any_field(models.CharField(max_length=10))
    >>> type(result)
    <type 'str'>
    """
    min_length = kwargs.get('min_length', 1)
    max_length = kwargs.get('max_length', field.max_length)
    return xunit.any_string(min_length=min_length, max_length=max_length)


@any_field.register(models.CommaSeparatedIntegerField)
def any_commaseparatedinteger_field(field, **kwargs):
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


@any_field.register(models.DateField)
def any_date_field(field, **kwargs):
    """
    Return random value for DateField,
    skips auto_now and auto_now_add fields

    >>> result = any_field(models.DateField())
    >>> type(result)
    <type 'datetime.date'>
    """
    if field.auto_now or field.auto_now_add:
        return None
    from_date = kwargs.get('from_date', date(1990, 1, 1))
    to_date = kwargs.get('to_date', date.today())
    return xunit.any_date(from_date=from_date, to_date=to_date)


@any_field.register(models.DateTimeField)
def any_datetime_field(field, **kwargs):
    """
    Return random value for DateTimeField,
    skips auto_now and auto_now_add fields

    >>> result = any_field(models.DateTimeField())
    >>> type(result)
    <type 'datetime.datetime'>
    """
    from_date = kwargs.get('from_date', datetime(1990, 1, 1))
    to_date = kwargs.get('to_date', datetime.today())
    return xunit.any_datetime(from_date=from_date, to_date=to_date)


@any_field.register(models.DecimalField)
def any_decimal_field(field, **kwargs):
    """
    Return random value for DecimalField

    >>> result = any_field(models.DecimalField(max_digits=5, decimal_places=2))
    >>> type(result)
    <class 'decimal.Decimal'>
    """
    min_value = kwargs.get('min_value', 0)
    max_value = kwargs.get('max_value',
                           Decimal('%s.%s' % ('9'*(field.max_digits-field.decimal_places),
                                              '9'*field.decimal_places)))
    decimal_places = kwargs.get('decimal_places', field.decimal_places)
    return xunit.any_decimal(min_value=min_value, max_value=max_value,
                             decimal_places = decimal_places)


@any_field.register(models.EmailField)
def any_email_field(field, **kwargs):
    """
    Return random value for EmailField

    >>> result = any_field(models.EmailField())
    >>> type(result)
    <type 'str'>
    >>> re.match(r"(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)", result, re.IGNORECASE) is not None
    True
    """
    return "%s@%s.%s" % (xunit.any_string(max_length=10),
                         xunit.any_string(max_length=10),
                         xunit.any_string(min_length=2, max_length=3))


@any_field.register(models.FloatField)
def any_float_field(field, **kwargs):
    """
    Return random value for FloatField

    >>> result = any_field(models.FloatField())
    >>> type(result)
    <type 'float'>
    """
    min_value = kwargs.get('min_value', 1)
    max_value = kwargs.get('max_value', 100)
    precision = kwargs.get('precision', 3)
    return xunit.any_float(min_value=min_value, max_value=max_value, precision=precision)


@any_field.register(models.FileField)
def any_file_field(field, **kwargs):
    """
    Lookup for nearest existing file

    """
    def get_some_file(path):
        subdirs, files = field.storage.listdir(path)

        if files:
            result_file = random.choice(files)
            instance = field.storage.open("%s/%s" % (path, result_file)).file
            return FieldFile(instance, field, result_file)

        for subdir in subdirs:
            result = get_some_file("%s/%s" % (path, subdir))
            if result:
                return result
            
    result = get_some_file(field.upload_to)

    if result is None and not field.null:
        raise TypeError("Can't found file in %s for non nullable FileField" % field.upload_to)
    return result


@any_field.register(models.FilePathField)
def any_filepath_field(field, **kwargs):
    """
    Lookup for nearest existing file

    """
    def get_some_file(path):
        subdirs, files = [], []
        for entry in os.listdir(path):
            entry_path = os.path.join(path, entry)
            if os.path.isdir(entry_path):
                subdirs.append(entry_path)
            else:
                if not field.match or re.match(field.match,entry):
                    files.append(entry_path)

        if files:
            return random.choice(files)
        
        if field.recursive:
            for subdir in subdirs:
                result = get_some_file(subdir)
                if result:
                    return result

    result = get_some_file(field.path)
    if result is None and not field.null:
        raise TypeError("Can't found file in %s for non nullable FilePathField" % field.path)
    return result


@any_field.register(models.IPAddressField)
def any_ipaddress_field(field, **kwargs):
    """
    Return random value for IPAddressField
    >>> result = any_field(models.IPAddressField())
    >>> type(result)
    <type 'str'>
    >>> from django.core.validators import ipv4_re
    >>> re.match(ipv4_re, result) is not None
    True
    """
    nums = [str(xunit.any_int(min_value=0, max_value=255)) for _ in xrange(0, 4)]
    return ".".join(nums)


@any_field.register(models.NullBooleanField)
def any_nullboolean_field(field, **kwargs):
    """
    Return random value for NullBooleanField
    >>> result = any_field(models.NullBooleanField())
    >>> result in [None, True, False]
    True
    """
    return random.choice([None, True, False])


@any_field.register(models.PositiveSmallIntegerField)
def any_positivesmallinteger_field(field, **kwargs):
    """
    Return random value for PositiveSmallIntegerField
    >>> result = any_field(models.PositiveSmallIntegerField())
    >>> type(result)
    <type 'int'>
    >>> result < 256, result > 0
    (True, True)
    """
    min_value = kwargs.get('min_value', 1)
    max_value = kwargs.get('max_value', 255)
    return xunit.any_int(min_value=min_value, max_value=max_value)


@any_field.register(models.SlugField)
def any_slug_field(field, **kwargs):
    """
    Return random value for SlugField
    >>> result = any_field(models.SlugField())
    >>> type(result)
    <type 'str'>
    >>> from django.core.validators import slug_re
    >>> re.match(slug_re, result) is not None
    True
    """
    letters = ascii_letters + digits + '_-'
    return xunit.any_string(letters = letters, max_length = field.max_length)


@any_field.register(models.SmallIntegerField)
def any_smallinteger_field(field, **kwargs):
    """
    Return random value for SmallIntegerValue
    >>> result = any_field(models.SmallIntegerField())
    >>> type(result)
    <type 'int'>
    >>> result > -256, result < 256
    (True, True)
    """
    min_value = kwargs.get('min_value', -255)
    max_value = kwargs.get('max_value', 255)
    return xunit.any_int(min_value=min_value, max_value=max_value)


@any_field.register(models.IntegerField)
def any_integer_field(field, **kwargs):
    """
    Return random value for IntegerField
    >>> result = any_field(models.IntegerField())
    >>> type(result)
    <type 'int'>
    """
    min_value = kwargs.get('min_value', -10000)
    max_value = kwargs.get('max_value', 10000)
    return xunit.any_int(min_value=min_value, max_value=max_value)


@any_field.register(models.TextField)
def any_text_field(field, **kwargs):
    """
    Return random 'lorem ipsum' Latin text
    >>> result = any_field(models.TextField())
    >>> from django.contrib.webdesign.lorem_ipsum import COMMON_P
    >>> result[0] == COMMON_P
    True
    """
    return paragraphs(10)


@any_field.register(models.URLField)
def any_url_field(field, **kwargs):
    """
    Return random value for URLField
    >>> result = any_field(models.URLField())
    >>> from django.core.validators import URLValidator
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
    url = kwargs.get('url', url)
    return choice(url)


@any_field.register(models.TimeField)
def any_time_field(field, **kwargs):
    """
    Return random value for TimeField
    >>> result = any_field(models.TimeField())
    >>> type(result)
    <type 'datetime.time'>
    """
    return time(
        xunit.any_int(min_value=0, max_value=23),
        xunit.any_int(min_value=0, max_value=59),
        xunit.any_int(min_value=0, max_value=59))


@any_field.register(models.ForeignKey)
def any_foreignkey_field(field, **kwargs):
    return any_model(field.rel.to, **kwargs)


@any_field.register(models.OneToOneField)
def any_onetoone_field(field, **kwargs):
    return any_model(field.rel.to, **kwargs)


def _fill_model_fields(model, **kwargs):
    model_fields, fields_args = split_model_kwargs(kwargs)
    for field in model._meta.fields:
        if field.name in model_fields:
            if isinstance(kwargs[field.name], Q):
                """
                Lookup ForeingKey field in db
                """
                key_field = model._meta.get_field(field.name)
                value = key_field.rel.to.objects.get(kwargs[field.name])
                setattr(model, field.name, value)
            else:
                setattr(model, field.name, kwargs[field.name])
        elif isinstance(field, models.OneToOneField) and field.rel.parent_link:
            """
            skip link to parent instance
            """
        elif isinstance(field, models.fields.AutoField):
            """
            skip primary key field
            """
        else:
            setattr(model, field.name, any_field(field, **fields_args[field.name]))


@any_model.register_default
def any_model_default(model_cls, **kwargs):
    result = model_cls()

    attempts = 10
    while True:
        try:
            _fill_model_fields(result, **kwargs)
            result.full_clean()
            result.save()
            return result
        except (IntegrityError, ValidationError):
            attempts -= 1
            if not attempts:
                raise

