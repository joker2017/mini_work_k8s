# tests.py
from .test_utils import BaseTestCase
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient

from account.serializers import AccountSerializer, AccountSerializerRegistr
# Предположим, что у вас есть такие модули
from account.services import create_account_number

# Имитация модели Account для тестов
mock_account = MagicMock()

# Тесты для API, использующие мокирование вместо реальной базы данных
class AccountAPITestCase(BaseTestCase):
    @patch('account.models.Account.objects.all')
    def test_account_list(self, mock_all):
        mock_all.return_value = [mock_account]
        client = APIClient()
        response = client.get('/account/list/')
        self.assertEqual(response.status_code, 200)
        mock_all.assert_called_once()

    @patch('account.services.create_account_number')
    @patch('account.serializers.AccountSerializerRegistr.save')
    def test_account_create(self, mock_save, mock_create_account_number):
        mock_create_account_number.return_value = '1234567890'
        mock_save.return_value = mock_account
        client = APIClient()
        data = {'name': 'Test Account', 'balance': 1000}
        response = client.post('/account/create/', data, format='json')
        self.assertEqual(response.status_code, 201)
        mock_create_account_number.assert_called_once()
        mock_save.assert_called_once()

# Тесты для сервиса создания номера аккаунта
class CreateAccountNumberTestCase(BaseTestCase):
    @patch('account.models.Account.objects.filter')
    def test_create_account_number_success(self, mock_filter):
        mock_filter.return_value.exists.return_value = False
        account_number = create_account_number()
        self.assertEqual(len(account_number), 20)
        self.assertTrue(account_number.isdigit())
        mock_filter.assert_called_once_with(id=account_number)

# Тесты для сериализаторов
class AccountSerializerTestCase(BaseTestCase):
    def test_account_serializer_fields(self):
        account_data = {'name': 'Test Account', 'balance': 1000}
        serializer = AccountSerializer(data=account_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(set(serializer.validated_data.keys()), set(['name', 'balance']))

    def test_account_serializer_registr_save(self):
        account_registr_data = {'name': 'Test Account', 'balance': 1000}
        serializer = AccountSerializerRegistr(data=account_registr_data)
        with patch.object(AccountSerializerRegistr, 'save', return_value=mock_account) as mock_save:
            self.assertTrue(serializer.is_valid())
            serializer.save()
            mock_save.assert_called_once()
