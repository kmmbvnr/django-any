# -*- coding: utf-8 -*-
"""
Django forms data generators

"""
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
            return _wrapper(func)
        return _wrapper
    
    def decorator(self, impl=None):
        """
        Decorator for register decorators
        """
        self.__call__ = impl(self.__call__)

    def __call__(self, *args, **kwargs):
        if not len(args):
            raise TypeError('Field instance are not provided')

        field_type = args[0].__class__

        function = self.registry.get(field_type)

        if function is None:
            raise TypeError("no match %s" % field_type)

        return function(*args, **kwargs)

any_form_field = FormFieldDataFactory()


@any_form_field.register(forms.BooleanField)
def boolean_field_data(field, **kwargs):
    """
    Return random value for BooleanField

    >>> result = any_form_field(forms.BooleanField())
    >>> type(result)
    <type 'bool'>
    """
    return xunit.any_boolean()

