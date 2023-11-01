from django.db import IntegrityError
from django.test import TestCase, SimpleTestCase

from ..models import Users, Account
from django.test import SimpleTestCase

class UsersModelTest(SimpleTestCase):
    def setUp(self):
        self.user_data = {
            'id': '12345',
            'full_names': 'John Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'mypassword',
        }

    def test_create_user(self):
        user = Users.objects.create(**self.user_data)
        self.assertEqual(user.id, '12345')
        self.assertEqual(user.full_names, 'John Doe')
        self.assertEqual(user.username, 'johndoe')
        self.assertEqual(user.email, 'johndoe@example.com')
        self.assertEqual(user.password, 'hashed_password')

    def test_unique_username(self):
        Users.objects.create(**self.user_data)  # Create a user with the same username
        with self.assertRaises(IntegrityError):
            Users.objects.create(**self.user_data)


class AccountModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'id': '12345',
            'full_names': 'John Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'hashed_password',
        }
        self.user = Users.objects.create(**self.user_data)

        self.account_data = {
            'id': 'account123',
            'balance': 100.0,
            'usernameid': self.user,
        }

    def test_create_account(self):
        account = Account.objects.create(**self.account_data)
        self.assertEqual(account.id, 'account123')
        self.assertEqual(account.balance, 100.0)
        self.assertEqual(account.usernameid, self.user)

    def test_default_balance(self):
        account = Account.objects.create(id='account456', usernameid=self.user)
        self.assertEqual(account.balance, 0.0)
