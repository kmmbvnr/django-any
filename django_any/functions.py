#-*- coding: utf-8 -*-
# pylint: disable=E0102, W0613
"""
Additional functions for django-any
"""

def valid_choices(choices):
    for key, value in choices:
        if isinstance(value, (list, tuple)):
            for key, _ in value:
                yield key
        else:
            yield key
