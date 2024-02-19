from django.test import TestCase, override_settings
from rest_framework.test import APITestCase
from django.db import connection
from unittest.mock import patch
from account.models import Account
from account.serializers import AccountSerializer, AccountSerializerRegistr
from account.services import create_account_number

# Функция-блокировщик, которая будет вызывать исключение при любых попытках выполнить запрос к базе данных
def blocker(execute, sql, params, many, context):
    raise Exception("Access to database blocked here. SQL: {}, Params: {}".format(sql, params))

@override_settings(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)
class BaseTestCase(TestCase):
    pass

class AccountAPITestCase(APITestCase):
    @patch('account.views.Account.objects.all')
    def test_account_list(self, mock_all):
        mock_all.return_value = []
        with connection.execute_wrapper(blocker):
            response = self.client.get('/account/list/')
            self.assertEqual(response.status_code, 200)
            mock_all.assert_called_once()

    @patch('account.views.AccountSerializer')
    @patch('account.views.create_account_number')
    def test_account_create(self, mock_create_account_number, mock_serializer):
        mock_account = Account(name="Test Account", balance=1000)
        mock_serializer.return_value.is_valid.return_value = True
        mock_serializer.return_value.save.return_value = mock_account
        mock_create_account_number.return_value = '1234567890'

        with connection.execute_wrapper(blocker):
            data = {'name': 'Test Account', 'balance': 1000}
            response = self.client.post('/account/create/', data, format='json')
            self.assertEqual(response.status_code, 201)
            mock_create_account_number.assert_called_once()
            mock_serializer.assert_called_once_with(data=data)

class CreateAccountNumberTestCase(TestCase):
    @patch('account.services.Account.objects.filter')
    def test_create_account_number_success(self, mock_filter):
        mock_filter.return_value.exists.return_value = False
        with connection.execute_wrapper(blocker):
            account_number = create_account_number()
            self.assertEqual(len(account_number), 10)  # Assuming account_number length is 10 for simplicity
            self.assertTrue(account_number.isdigit())
            mock_filter.assert_called_once_with(account_number=account_number)

class AccountSerializerTestCase(TestCase):
    def test_account_serializer_fields(self):
        with connection.execute_wrapper(blocker):
            account_data = {'name': 'Test Account', 'balance': 1000}
            serializer = AccountSerializer(data=account_data)
            self.assertTrue(serializer.is_valid())
            self.assertEqual(set(serializer.validated_data.keys()), {'name', 'balance'})

    @patch('account.models.Account.save', autospec=True)
    def test_account_serializer_registr_save(self, mock_save):
        with connection.execute_wrapper(blocker):
            account_registr_data = {'name': 'Test Account', 'balance': 1000}
            serializer = AccountSerializerRegistr(data=account_registr_data)
            self.assertTrue(serializer.is_valid())
            serializer.save()
            mock_save.assert_called_once()
