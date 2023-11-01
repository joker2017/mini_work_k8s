from django.test import TestCase
from ..services import create_account_number


class CreateAccountNumberTest(TestCase):
    def test_create_unique_account_number(self):
        account_numbers = set()
        for _ in range(10):
            account_number = create_account_number()
            self.assertNotIn(account_number, account_numbers)
            account_numbers.add(account_number)

    def test_create_account_number_length(self):
        account_number = create_account_number()
        self.assertEqual(len(account_number), 20)