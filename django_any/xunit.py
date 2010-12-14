#-*- coding: utf-8 -*-
"""
The python basic types generators
"""
import random
from string import ascii_letters
from datetime import date, datetime, timedelta
from decimal import Decimal

def weighted_choice(choices):
    """
    Supposes that choices is sequence of two elements items,
    where first one is the probability and second is the
    result object or callable

    >>> result = weighted_choice([(20,'x'), (100, 'y')])
    >>> result in ['x', 'y']
    True
    """
    total = sum([weight for (weight, _) in choices])
    i = random.randint(0, total - 1)
    for weight, choice in choices:
        i -= weight
        if i < 0: 
            if callable(choice):
                return choice()
            return choice
    raise Exception('Bug')


def any_boolean():
    """
    Returns True or False
    
    >>> result = any_boolean()
    >>> type(result)
    <type 'bool'>
    """
    return random.choice([True, False])


def any_int(min_value=0, max_value=100, **kwargs):
    """
    Return random integer from the selected range

    >>> result = any_int(min_value=0, max_value=100)
    >>> type(result)
    <type 'int'>
    >>> result in range(0,101)
    True

    """
    return random.randint(min_value, max_value)


def any_float(min_value=0, max_value=100, precision=2):
    """
    Returns random float
    
    >>> result = any_float(min_value=0, max_value=100, precision=2)
    >>> type(result)
    <type 'float'>
    >>> result >=0 and result <= 100
    True

    """
    return round(random.uniform(min_value, max_value), precision)


def any_letter(letters = ascii_letters, **kwargs):
    """
    Return random letter

    >>> result = any_letter(letters = ascii_letters)
    >>> type(result)
    <type 'str'>
    >>> len(result)
    1
    >>> result in ascii_letters
    True

    """
    return random.choice(letters)


def any_string(letters = ascii_letters, min_length=3, max_length=100):
    """
    Return string with random content

    >>> result = any_string(letters = ascii_letters, min_length=3, max_length=100)
    >>> type(result)
    <type 'str'>
    >>> len(result) in range(3,101)
    True
    >>> any([c in ascii_letters for c in result])
    True
    """
    
    length = random.randint(min_length, max_length)
    letters = [any_letter(letters=letters) for _ in range(0, length)]
    return "".join(letters)


def any_date(from_date=date(1990, 1, 1), to_date=date.today()):
    """
    Return random date from the [from_date, to_date] interval

    >>> result = any_date(from_date=date(1990,1,1), to_date=date(1990,1,3))
    >>> type(result)
    <type 'datetime.date'>
    >>> result >= date(1990,1,1) and result <= date(1990,1,3)
    True
    """
    days = any_int(min_value=0, max_value=(to_date - from_date).days)

    return from_date + timedelta(days=days)


def any_datetime(from_date=datetime(1990, 1, 1), to_date=datetime.now()):
    """
    Return random datetime from the [from_date, to_date] interval

    >>> result = any_datetime(from_date=datetime(1990,1,1), to_date=datetime(1990,1,3))
    >>> type(result)
    <type 'datetime.datetime'>
    >>> result >= datetime(1990,1,1) and result <= datetime(1990,1,3)
    True
    """
    days = any_int(min_value=0, max_value=(to_date - from_date).days-1)
    time = timedelta(seconds=any_int(min_value=0, max_value=24*3600-1))

    return from_date + timedelta(days=days) + time


def any_decimal(min_value=Decimal(0), max_value=Decimal('99.99'), decimal_places=2):
    """
    Return random decimal from the [min_value, max_value] interval

    >>> result = any_decimal(min_value=0.999, max_value=3, decimal_places=3)
    >>> type(result)
    <class 'decimal.Decimal'>
    >>> result >= Decimal('0.999') and result <= Decimal(3)
    True
    """
    return Decimal(str(any_float(min_value=float(min_value),
                                 max_value=float(max_value),
                                 precision=decimal_places)))

