# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.test import TestCase
from django_any import any_model, xunit
from django_any.test import WithTestDataSeed, without_random_seed, with_seed

class SimpleModel(models.Model):
    name = models.CharField(max_length=5)

    class Meta:
        app_label = 'django_any'


class ModelWithForeignKey(models.Model):
    name = models.CharField(max_length=5)
    simple = models.ForeignKey(SimpleModel)

    class Meta:
        app_label = 'django_any'


class ModelWithOneToOneField(models.Model):
    name = models.CharField(max_length=5)
    simple = models.OneToOneField(SimpleModel)

    class Meta:
        app_label = 'django_any'


class ModelWithOneChoice(models.Model):
    CHOICES = [('N', 'No')]
    choice = models.CharField(max_length=1, choices=CHOICES, unique=True)

    class Meta:
        app_label = 'django_any'


class ModelWithTwoChoices(models.Model):
    CHOICES = [('Y', 'Yes'),
               ('N', 'No')]
    choice = models.CharField(max_length=1, choices=CHOICES, unique=True)

    class Meta:
        app_label = 'django_any'


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(u'%s is not an even number' % value)


class ModelWithValidation(models.Model):
    even_field = models.PositiveIntegerField(validators=[validate_even])

    class Meta:
        app_label = 'django_any'


class ModelWithFileField(models.Model):
    content = models.FileField(upload_to='.')
    content_path = models.FilePathField(path=settings.MEDIA_ROOT, recursive=True)

    class Meta:
        app_label = 'django_any'


class ModelWithConstraint(models.Model):
    """
    Validates that start_time is always before end_time
    """
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError('start_time could not be after end_time')

    class Meta:
        app_label = 'django_any'


class ModelWithConstraintOnForeignKey(models.Model):
    timestamp = models.ForeignKey(ModelWithConstraint)

    class Meta:
        app_label = 'django_any'


@any_model.register(ModelWithConstraint)
def any_model_with_constraint(model_cls, **kwargs):
    start_time = kwargs.get('start_time')
    end_time = kwargs.get('end_time')

    kwargs['start_time'] = start_time or xunit.any_datetime(to_date=end_time)
    kwargs['end_time'] = end_time or xunit.any_datetime(from_date=kwargs['start_time'])

    return any_model.default(model_cls, **kwargs)


class TestAnyModel(TestCase):
    def test_simple_model_creation(self):
        result = any_model(SimpleModel)
        self.assertEqual(type(result), SimpleModel)
        self.assertTrue(result.name is not None)

    def test_foreign_key_creation(self):
        result = any_model(ModelWithForeignKey)
        self.assertEqual(type(result), ModelWithForeignKey)
        self.assertEqual(type(result.simple), SimpleModel)
        self.assertTrue(result.name is not None)
        self.assertTrue(result.simple.name is not None)

    def test_onetoonefield_creation(self):
        result = any_model(ModelWithOneToOneField)
        self.assertEqual(type(result), ModelWithOneToOneField)
        self.assertEqual(type(result.simple), SimpleModel)
        self.assertTrue(result.name is not None)
        self.assertTrue(result.simple.name is not None)

    def test_set_nested_fields(self):
        result = any_model(ModelWithForeignKey, simple__name='Name')
        self.assertEqual('Name', result.simple.name)

    def test_constraint_succeed(self):
        result = any_model(ModelWithConstraint)
        self.assertTrue(result.start_time <= result.end_time)

    def test_foreignkey_constraint_succeed(self):
        result = any_model(ModelWithConstraintOnForeignKey)
        self.assertTrue(result.timestamp.start_time <= result.timestamp.end_time)
        

class TestQObjectsSupport(TestCase):
    def test_simple_lookup_succeed(self):
        simple = any_model(SimpleModel)
        result = any_model(ModelWithForeignKey, simple=Q(pk=simple.pk))
        self.assertEqual(simple, result.simple)
        

class TestUniqueConstrainViolations(TestCase):
    def test_fail_if_no_choices(self):
        ModelWithOneChoice.objects.create(choice='N')
        self.assertRaises(ValidationError, any_model, ModelWithOneChoice)

    def test_unique_generation_succedd(self):
        ModelWithTwoChoices.objects.create(choice='N')
        
        result = any_model(ModelWithTwoChoices)
        self.assertEqual('Y', result.choice)


class TestValidationPassed(TestCase):
    def test_even_field_generation(self):
        result = any_model(ModelWithValidation)
        validate_even(result.even_field)


class TestAnyModelFieldConstraints(TestCase):
    __metaclass__ = WithTestDataSeed

    @without_random_seed
    @with_seed(1)
    def test_char_min_length(self):
        result = any_model(SimpleModel, name__min_length=3)
        self.assertTrue(len(result.name) >= 3)

# Disabled, since it is require local files
#class TestFilesFields(TestCase):
#    def test_model_with_filefield_save_success(self):
#        result = any_model(ModelWithFileField)

