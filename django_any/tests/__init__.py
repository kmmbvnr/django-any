# -*- coding: utf-8 -*-
import doctest
from unittest import TestSuite, defaultTestLoader
from django_any.tests import any_field_tests, any_forms_tests, \
    any_model_tests, any_user_tests, test_client_tests, \
    test_set_seed_tests

def suite():
    result = TestSuite()

    result.addTest(doctest.DocTestSuite('django_any.xunit'))
    result.addTest(doctest.DocTestSuite('django_any.models'))
    result.addTest(doctest.DocTestSuite('django_any.forms'))
    result.addTest(defaultTestLoader.loadTestsFromModule(any_field_tests))
    result.addTest(defaultTestLoader.loadTestsFromModule(any_model_tests))
    result.addTest(defaultTestLoader.loadTestsFromModule(any_forms_tests))
    result.addTest(defaultTestLoader.loadTestsFromModule(any_user_tests))
    result.addTest(defaultTestLoader.loadTestsFromModule(test_client_tests))
    result.addTest(defaultTestLoader.loadTestsFromModule(test_set_seed_tests))

    return result
