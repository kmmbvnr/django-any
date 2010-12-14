# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Permission, Group
from django_any import any_model

def any_user(password=None, permissions=[], groups=[], **kwargs):
    """
    Shortcut for creating Users

    Permissions could be a list of permission names

    If not specified, creates active, non superuser 
    and non staff user
    """

    is_active = kwargs.pop('is_active', True)
    is_superuser = kwargs.pop('is_superuser', False)
    is_staff = kwargs.pop('is_staff', False)

    user = any_model(User, is_active = is_active, is_superuser = is_superuser,
                     is_staff = is_staff, **kwargs)

    for group_name in groups :
        group = Group.objects.get(name=group_name)
        user.groups.add(group)

    for permission_name in permissions:
        app_label, codename = permission_name.split('.')
        permission = Permission.objects.get(
            content_type__app_label=app_label,
            codename=codename)
        user.user_permissions.add(permission)

    if password:
        user.set_password(password)
    
    user.save()
    return user

