# -*- coding: utf-8 -*-
import doctest
from unittest import TestSuite, defaultTestLoader
from django_any.tests import any_field_tests, any_forms_tests, \
    any_model_tests, any_user_tests

def suite():
     suite = TestSuite()
     suite.addTest(defaultTestLoader.loadTestsFromModule(any_field_tests))
     suite.addTest(defaultTestLoader.loadTestsFromModule(any_model_tests))
     suite.addTest(defaultTestLoader.loadTestsFromModule(any_forms_tests))
     suite.addTest(defaultTestLoader.loadTestsFromModule(any_user_tests))
     suite.addTest(doctest.DocTestSuite('django_any.xunit'))
     suite.addTest(doctest.DocTestSuite('django_any.models'))
     suite.addTest(doctest.DocTestSuite('django_any.forms'))

     return suite

