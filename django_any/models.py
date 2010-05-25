#-*- coding: utf-8 -*-
from collections import defaultdict
from django.db import models

from django_any import fields, xunit
from django_any.multimethod import multimethod


@multimethod(models.ForeignKey)
def any(field, **kwargs):
    if field.null and xunit.any_boolean():
        return None
    return any_model(field.rel.to, **kwargs)


def split_model_kwargs(kw):
    model_fields = {}
    fields_agrs = defaultdict(lambda : {})
    
    for key in kw.keys():
        if '__' in key:
            field, _, subfield = key.partition('__')
            fields_agrs[field][subfield] = kw[key]
        else:
            model_fields[key] = kw[key]

    return model_fields, fields_agrs
    

def any_model(model_cls, **kwargs):
    result = model_cls()

    model_fields, fields_args = split_model_kwargs(kwargs)
    for field in model_cls._meta.fields:
        if field.name in model_fields:
            setattr(result, field.name, kwargs[field.name])
        elif not isinstance(field, models.fields.AutoField):
            setattr(result, field.name, fields.any(field, **fields_args[field.name]))

    result.save()
    return result

