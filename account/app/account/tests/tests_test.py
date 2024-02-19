from unittest.mock import patch, MagicMock

from django.test import SimpleTestCase
from rest_framework.test import APITestCase

# from account.app.account.serializers import AccountSerializer, AccountSerializerRegistr
#from account.app.account.serializers import AccountSerializer, AccountSerializerRegistr
from account.serializers import AccountSerializer, AccountSerializerRegistr
# Предположим, что у вас есть такие модули
from account.services import create_account_number

# Имитация модели Account для тестов
mock_account = MagicMock()

# Тесты для API, использующие мокирование вместо реальной базы данных
class AccountAPITestCase(APITestCase):
    @patch('account.app.account.models.Account.objects.all')
    def test_account_list(self, mock_all):
        # Настройка мока
        mock_all.return_value = [mock_account]

        # Тестовый запрос к API
        response = self.client.get('/account/list/')

        # Проверки
        self.assertEqual(response.status_code, 200)
        mock_all.assert_called_once()

    @patch('account.app.account.services.create_account_number')
    @patch('account.app.account.serializers.AccountSerializerRegistr.save')
    def test_account_create(self, mock_save, mock_create_account_number):
        # Настройка моков
        mock_create_account_number.return_value = '1234567890'
        mock_save.return_value = mock_account

        # Тестовый запрос к API
        data = {'name': 'Test Account', 'balance': 1000}
        response = self.client.post('/account/create/', data, format='json')

        # Проверки
        self.assertEqual(response.status_code, 201)
        mock_create_account_number.assert_called_once()
        mock_save.assert_called_once()

# Тесты для сервиса создания номера аккаунта
class CreateAccountNumberTestCase(SimpleTestCase):
    @patch('account.app.account.models.Account.objects.filter')
    def test_create_account_number_success(self, mock_filter):
        # Настройка мока
        mock_filter.return_value.exists.return_value = False

        # Вызов тестируемой функции
        account_number = create_account_number()

        # Проверки
        self.assertEqual(len(account_number), 20)
        self.assertTrue(account_number.isdigit())
        mock_filter.assert_called_once_with(id=account_number)

# Тесты для сериализаторов
class AccountSerializerTestCase(SimpleTestCase):
    def test_account_serializer_fields(self):
        # Имитация данных аккаунта
        account_data = {'name': 'Test Account', 'balance': 1000}

        # Создание сериализатора с данными
        serializer = AccountSerializer(data=account_data)

        # Проверка валидности сериализатора
        self.assertTrue(serializer.is_valid())
        self.assertEqual(set(serializer.validated_data.keys()), set(['name', 'balance']))

    def test_account_serializer_registr_save(self):
        # Имитация данных для регистрации аккаунта
        account_registr_data = {'name': 'Test Account', 'balance': 1000}

        # Создание сериализатора с данными
        serializer = AccountSerializerRegistr(data=account_registr_data)

        # Проверка валидности сериализатора и вызов save (мокируется)
        with patch.object(AccountSerializerRegistr, 'save', return_value=mock_account) as mock_save:
            self.assertTrue(serializer.is_valid())
            serializer.save()
            mock_save.assert_called_once()
