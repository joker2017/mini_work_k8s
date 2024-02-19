# test_utils.py
from django.test import TestCase, override_settings

@override_settings(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    }
)
class BaseTestCase(TestCase):
    pass
