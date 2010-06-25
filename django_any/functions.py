#-*- coding: utf-8 -*-
"""
Additional functions for django-any
"""

def valid_choices(choices):
    """
    Return list of choices's key
    """
    for key, value in choices:
        if isinstance(value, (list, tuple)):
            for key, _ in value:
                yield key
        else:
            yield key
