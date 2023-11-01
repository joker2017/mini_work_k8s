from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Users, Account
from .services import create_account_number
from hashlib import sha256

from django.db import IntegrityError
from django.db.models.deletion import ProtectedError


class UserModelTest(TestCase):

    def setUp(self):
        self.user_data = {
            "id": "test",
            "full_names": "Test User",
            "username": "testuser",
            "email": "test@user.com",
            "password": "testpassword"
        }

    def test_user_creation(self):
        user = Users.objects.create(**self.user_data)
        self.assertEqual(Users.objects.count(), 1)
        self.assertEqual(user.full_names, "Test User")

    def test_password_hashing(self):
        user = Users.objects.create(**self.user_data)
        self.assertNotEqual(user.password, "testpassword")
        self.assertEqual(user.password, sha256("testpassword".encode('utf-8')).hexdigest())

    def test_user_id_uniqueness(self):
        Users.objects.create(**self.user_data)
        with self.assertRaises(IntegrityError):
            Users.objects.create(**self.user_data)


class AccountModelTest(TestCase):

    def setUp(self):
        self.user_data = {
            "id": "testuser12",
            "full_names": "Test User",
            "username": "testuser",
            "email": "test@user.com",
            "password": "testpassword"
        }
        self.user = Users.objects.create(**self.user_data)
        self.account_data = {
            "id": "testacco",
            "balance": 100.50,
            "usernameid": self.user
        }

    def test_account_creation(self):
        account = Account.objects.create(**self.account_data)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(account.balance, 100.50)

    def test_account_user_relationship(self):
        account = Account.objects.create(**self.account_data)
        self.assertEqual(self.user.users.count(), 1)
        self.assertEqual(self.user.users.first(), account)

    def test_account_id_uniqueness(self):
        Account.objects.create(**self.account_data)
        with self.assertRaises(IntegrityError):
            Account.objects.create(**self.account_data)


class UserViewsTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "full_names": "Test User",
            "username": "testuser",
            "email": "test@user.com",
            "password": "testpassword"
        }
        self.user = Users.objects.create(**self.user_data)

    def test_user_creation(self):
        response = self.client.post(reverse('profile1'), self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Users.objects.count(), 2)

    def test_user_search(self):
        response = self.client.get(reverse('usersearch'), {'search': 'testuser'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)




