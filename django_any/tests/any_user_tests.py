# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.test import TestCase
from django_any import any_model
from django_any.contrib.auth import any_user


class TestPermission(models.Model):
    name = models.CharField(max_length=5)

    class Meta:
        app_label = 'django_any'


class TestCreateUser(TestCase):
    def test_raw_user_creation(self):
        result = any_model(User)
        self.assertEqual(type(result), User)


    def test_create_superuser(self):
        user = any_user(is_superuser=True)
        self.assertTrue(user.is_superuser)

    def test_create_with_permissions(self):
        user = any_user(permissions= ['django_any.add_testpermission',
                                      'django_any.delete_testpermission'])

        self.assertTrue(user.has_perm('django_any.add_testpermission'))
        self.assertTrue(user.has_perm('django_any.delete_testpermission'))
        self.assertFalse(user.has_perm('django_any.change_testpermission'))



