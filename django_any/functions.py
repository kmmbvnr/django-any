#-*- coding: utf-8 -*-
"""
Additional functions for django-any
"""

def valid_choices(choices):
    """
    Return list of choices's keys
    """
    for key, value in choices:
        if isinstance(value, (list, tuple)):
            for key, _ in value:
                yield key
        else:
            yield key


def split_model_kwargs(kw):
    """
    django_any birds language parser
    """
    from collections import defaultdict
    
    model_fields = {}
    fields_agrs = defaultdict(lambda : {})
    
    for key in kw.keys():
        if '__' in key:
            field, _, subfield = key.partition('__')
            fields_agrs[field][subfield] = kw[key]
        else:
            model_fields[key] = kw[key]

    return model_fields, fields_agrs


class ExtensionMethod(object):
    """
    Works like one parameter multimethod
    """
    def __init__(self, by_instance=False):
        self.registry = {}
        self.by_instance = by_instance
        self.default = None

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
    
    def register_default(self, func):
        self.default = func
        return func

    def decorator(self, impl):
        """
        Decorator for register decorators
        """
        self._create_value = impl(self._create_value)
        return impl

    def _create_value(self, *args, **kwargs):
        """
        Lowest value generator.

        Separated from __call__, because it seems that python
        cache __call__ reference on module import
        """
        if not len(args):
            raise TypeError('Object instance is not provided')

        if self.by_instance:
            field_type = args[0]
        else:
            field_type = args[0].__class__

        function = self.registry.get(field_type, self.default)

        if function is None:
            raise TypeError("no match %s" % field_type)

        return function(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self._create_value(*args, **kwargs)

