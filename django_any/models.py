#-*- coding: utf-8 -*-
from collections import defaultdict
from django.core.exceptions import ValidationError
from django.db import models, IntegrityError

from django_any.xunit import any_boolean
from django_any.fields import any_field
from django_any.multimethod import multimethod

@multimethod(models.ForeignKey)
def any_field(field, **kwargs):
    if field.null and any_boolean():
        return None
    return any_model(field.rel.to, **kwargs)


def _split_model_kwargs(kw):
    model_fields = {}
    fields_agrs = defaultdict(lambda : {})
    
    for key in kw.keys():
        if '__' in key:
            field, _, subfield = key.partition('__')
            fields_agrs[field][subfield] = kw[key]
        else:
            model_fields[key] = kw[key]

    return model_fields, fields_agrs
    

def _fill_model_fields(model, **kwargs):
    model_fields, fields_args = _split_model_kwargs(kwargs)
    for field in model._meta.fields:
        if field.name in model_fields:
            setattr(model, field.name, kwargs[field.name])
        elif not isinstance(field, models.fields.AutoField):
            setattr(model, field.name, any_field(field, **fields_args[field.name]))


def any_model(model_cls, **kwargs):
    result = model_cls()
    
    attempts = 10
    while True:
        try:
            _fill_model_fields(result, **kwargs)
            result.full_clean()
            result.save()            
            return result
        except (IntegrityError, ValidationError):
            attempts -=1
            if not attempts:
                raise

