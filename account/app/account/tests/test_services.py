from django.test import TestCase, SimpleTestCase
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from ..models import Account
from ..services import create_account_number


class CreateAccountNumberTest(SimpleTestCase):
    def test_unique_account_number(self):
        account1 = User.objects.create(id=get_random_string(20, "0123456789"))
        account2 = Account.objects.create(id=get_random_string(20, "0123456789"))

        new_account_number = create_account_number()

        self.assertNotIn(new_account_number, [account1.id, account2.id])

    def test_account_number_length(self):
        new_account_number = create_account_number()

        self.assertEqual(len(new_account_number), 20)
